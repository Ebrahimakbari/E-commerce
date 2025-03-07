from celery import shared_task
from utils import send_otp_by_email, send_otp_by_phone


@shared_task
def send_otp_by_email_async(email, link, expire_date): 
    send_otp_by_email(email, link, expire_date)


@shared_task
def send_otp_by_phone_async(phone_number, code):
    send_otp_by_phone(phone_number, code)