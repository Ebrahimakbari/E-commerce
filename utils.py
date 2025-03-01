from django.core.mail import EmailMessage
import datetime
from django.utils import timezone
from accounts.models import OtpEmail, OtpPhoneNumber









def send_otp_by_phone(phone_number, code):
    pass


def send_otp_by_email(email, link):
    e_mail = EmailMessage('Verify Account', f'to verify email click on this link:{link}', to=[email])
    e_mail.send()


def create_otp_phone_number_instance(phone_number, code, expiration_minutes=5):
    expiration_time = timezone.now() + datetime.timedelta(minutes=expiration_minutes)
    otp = OtpPhoneNumber.objects.create(phone_number=phone_number, code=code, expires_at=expiration_time)
    otp.save()
    return otp


def create_otp_email_instance(email, token, expiration_minutes=5):
    expiration_time = timezone.now() + datetime.timedelta(minutes=expiration_minutes)
    otp = OtpEmail.objects.create(email=email, token=token, expires_at=expiration_time)
    otp.save()
    return otp


