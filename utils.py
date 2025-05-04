from django.core.mail import EmailMessage
import datetime
from django.utils import timezone
from accounts.models import OtpEmail, OtpPhoneNumber
from kavenegar import *
from decouple import config
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission, SAFE_METHODS

User = get_user_model()



class IsAdminUserMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_admin



def send_otp_by_phone(phone_number, code):
    try:
        api = KavenegarAPI(config("OTP_SMS_CODE"))
        params = {
            "sender": config("SENDER_PHONE"),
            "receptor": str(phone_number),
            "message": f"کد تایید شما : {code}",
        }
        response = api.sms_send(params)
    except APIException as e:
        print(e, response)
    except HTTPException as e:
        print(e, response)


def send_otp_by_email(email, link, expire_date):
    e_mail = EmailMessage(
        "Verify Account",
        f"to verify email click on this link:{link} \n token expires in {expire_date} minutes!",
        to=[email],
    )
    e_mail.send()


def create_otp_phone_number_instance(phone_number, code, expiration_minutes=5):
    expiration_time = timezone.now() + datetime.timedelta(minutes=expiration_minutes)
    otp = OtpPhoneNumber.objects.create(
        phone_number=phone_number, code=code, expires_at=expiration_time
    )
    otp.save()
    return otp


def create_otp_email_instance(email, token, expiration_minutes=5):
    expiration_time = timezone.now() + datetime.timedelta(minutes=expiration_minutes)
    otp = OtpEmail.objects.create(email=email, token=token, expires_at=expiration_time)
    otp.save()
    return otp


class MyBackend:
    def authenticate(phone_number=None, password=None):
        user = User.objects.filter(phone_number=phone_number)
        if user.exists() and user.first().check_password(password):
            return user.first()
        return None

    def get_user(user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class IsAdminUserOrReadOnly(BasePermission):
    """
    The request is admin as a user, or is a read-only request.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(
            request.user and
            request.user.is_staff
        )


class IsOwnerOrAdmin(BasePermission):
    """
    Object-level permission to only allow owners of an object or admin to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the request user is staff (admin)
        if request.user.is_staff:
            return True
        # Check if the request user is the owner of the object
        return obj.user == request.user