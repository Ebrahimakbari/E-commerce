from datetime import datetime, timedelta
from celery import shared_task
import pytz
from accounts.models import OtpEmail, OtpPhoneNumber
from utils import send_otp_by_email, send_otp_by_phone


@shared_task
def send_otp_by_email_async(email, link, expire_date): 
    send_otp_by_email(email, link, expire_date)


@shared_task
def send_otp_by_phone_async(phone_number, code):
    send_otp_by_phone(phone_number, code)
    

# celery beat task
@shared_task
def delete_expired_otps():
        expired_time = datetime.now(tz=pytz.timezone('Asia/Tehran')) - timedelta(minutes=5)
        OtpEmail.objects.filter(created__lt=expired_time).delete()
        OtpPhoneNumber.objects.filter(created__lt=expired_time).delete()