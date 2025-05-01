import random
import uuid
from rest_framework import serializers, status
from accounts import tasks
from accounts.models import CustomUser, OtpPhoneNumber, OtpEmail
from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import ValidationError
from utils import create_otp_email_instance, create_otp_phone_number_instance





class RegisterUserSerializer(serializers.ModelSerializer):
    choices = [
        (1, 'Email'),
        (2, 'SMS'),
    ]
    
    verification_method = serializers.ChoiceField(choices=choices, write_only=True, help_text='SMS/Email')
    class Meta:
        model = CustomUser
        fields = ['email', 'phone_number', 'password', 'first_name', 'last_name', 'verification_method']
        extra_kwargs = {
            'password':{'write_only':True}
        }
    
    def create(self, validated_data):
        validated_data.pop('verification_method')
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('verification_method')
        if 'password' in validated_data.keys():
            validated_data['password'] = make_password(validated_data['password'])
        return super().update(instance, validated_data)

    def save(self, **kwargs):
        request = self.context['request']
        verification_method = self.initial_data['verification_method']
        email = self.validated_data['email']
        phone_number = self.validated_data['phone_number']
        expire_date = 5
        if verification_method == 1:
            token = uuid.uuid4()
            link = (
                request.build_absolute_uri("/")
                + f"accounts/user-verification/{token}/"
            )
            tasks.send_otp_by_email_async.delay(email, link, expire_date)
            create_otp_email_instance(email, token, expire_date)

        elif verification_method == 2:
            code = random.randint(1000, 9999)
            tasks.send_otp_by_phone_async.delay(phone_number=phone_number, code=code)
            create_otp_phone_number_instance(phone_number, code, expire_date)
        
        else:
            raise ValidationError("Invalid verification method.", code=status.HTTP_400_BAD_REQUEST)
        return super().save(**kwargs)