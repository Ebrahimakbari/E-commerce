import random
import uuid
from rest_framework import serializers, status
from accounts import tasks
from accounts.models import CustomUser, OtpPhoneNumber, OtpEmail
from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from utils import create_otp_email_instance, create_otp_phone_number_instance, MyBackend
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


class RegisterUserSerializer(serializers.ModelSerializer):
    choices = [
        ("1", 'Email'),
        ("2", 'SMS'),
    ]

    verification_method = serializers.ChoiceField(
        choices=choices, write_only=True, help_text='SMS/Email')

    class Meta:
        model = CustomUser
        fields = ['email', 'phone_number', 'password',
                    'first_name', 'last_name', 'verification_method']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        validated_data.pop('verification_method')
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('verification_method')
        if 'password' in validated_data.keys():
            validated_data['password'] = make_password(
                validated_data['password'])
        return super().update(instance, validated_data)

    def save(self, **kwargs):
        request = self.context['request']
        verification_method = self.initial_data['verification_method']
        email = self.validated_data['email']
        phone_number = self.validated_data['phone_number']
        expire_date = 5
        if verification_method == "1":
            token = uuid.uuid4()
            link = (
                request.build_absolute_uri("/")
                + f"api/users/user-activation/email/{token}/"
            )
            tasks.send_otp_by_email_async.delay(email, link, expire_date)
            create_otp_email_instance(email, token, expire_date)

        elif verification_method == "2":
            code = random.randint(1000, 9999)
            tasks.send_otp_by_phone_async.delay(
                phone_number=phone_number, code=code)
            create_otp_phone_number_instance(phone_number, code, expire_date)

        else:
            raise ValidationError(
                "Invalid verification method.", code=status.HTTP_400_BAD_REQUEST)
        return super().save(**kwargs)


class SmsOtpSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11)
    code = serializers.IntegerField(max_value=10000, min_value=999)

    def validate(self, data):
        user = CustomUser.objects.filter(phone_number=data['phone_number'])
        otp_field = OtpPhoneNumber.objects.filter(
            phone_number=data['phone_number'], code=data['code'])
        if user.exists() and otp_field.exists():
            user = user.first()
            user.is_active = True
            otp_field.first().delete()
            user.save()
            return data
        raise ValidationError('Invalid Phone Number or Code!!',
                                code=status.HTTP_400_BAD_REQUEST)


class EmailOtpSerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate(self, data):
        otp_field = OtpEmail.objects.filter(token=data['token'])
        if otp_field.exists():
            otp_field = otp_field.first()
            user = CustomUser.objects.get(email=otp_field.email)
            user.is_active = True
            user.save()
            otp_field.delete()
            data['email'] = user.email
            return data
        raise ValidationError(
            'Invalid Token!!', code=status.HTTP_400_BAD_REQUEST)


class LoginUserSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        phone_number = data['phone_number']
        password = data['password']
        user = MyBackend.authenticate(
            phone_number=phone_number, password=password)
        if not user:
            raise AuthenticationFailed(
                'invalid credential!!', code=status.HTTP_400_BAD_REQUEST)
        if not user.is_active:
            raise AuthenticationFailed(
                'user not activated!!', code=status.HTTP_400_BAD_REQUEST)
        data['tokens'] = user.get_token()
        data['user-info'] = {
            'phone_number': str(user.phone_number),
            'first_name': str(user.first_name),
            'last_name': str(user.last_name),
            'email': str(user.email),
        }
        return data


class LogoutUserSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, data):
        try:
            RefreshToken(data['refresh']).blacklist()
        except TokenError:
            raise ValidationError(
                'bad token!', code=status.HTTP_400_BAD_REQUEST)
        return data


class ResetPasswordSerializer(serializers.Serializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate(self, data):
        password1 = data['password1']
        password2 = data['password2']
        if password2 and password1 and password1 == password2:
            request = self.context['request']
            user = request.user
            user.password = make_password(password1)
            user.save()
            return data
        raise ValidationError('mismatch passwords!!', code=status.HTTP_400_BAD_REQUEST)


