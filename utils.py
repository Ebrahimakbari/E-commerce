from django.core.mail import EmailMessage










def send_otp_by_phone(phone_number, code):
    pass


def send_otp_by_email(email, link):
    e_mail = EmailMessage('Verify Account', f'to verify email click on this link:{link}', to=email)
    e_mail.send()