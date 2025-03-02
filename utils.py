from django.core.mail import EmailMessage
import datetime
from django.utils import timezone
from accounts.models import OtpEmail, OtpPhoneNumber
from kavenegar import *
import decouple


def send_otp_by_phone(phone_number, code):
    try:
        api = KavenegarAPI(decouple.config("API_SMS_CODE"))
        params = {
            "sender": decouple.config("sender_phone"),
            "receptor": str(phone_number),
            "message": f"کد تایید شما : {code}",
        }
        api.sms_send(params)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)


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
