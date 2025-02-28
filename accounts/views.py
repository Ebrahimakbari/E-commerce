from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserVerificationForm
from django.views import View
from django.contrib import messages
from utils import send_otp_by_email, send_otp_by_phone
import uuid
import random
from .models import OtpEmail, OtpPhoneNumber, CustomUser




class UserRegistrationView(View):
    form_class = UserRegistrationForm

    def get(self, request):
        form = self.form_class()
        return render(request, "accounts/register.html", {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            verification_method = form.cleaned_data["verification_method"]
            email = form.cleaned_data["email"]
            phone_number = form.cleaned_data["phone_number"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            if verification_method == "email":
                token = uuid.uuid4()
                send_otp_by_email(email, token)
                link = request.build_absolute_uri(f"register-verification/{token}")
                OtpEmail.objects.create(email=email, link=link)
                redirect_method = 'register'

            else:
                code = random.randint(1000, 9999)
                send_otp_by_phone(phone_number=phone_number, code=code)
                OtpPhoneNumber.objects.create(phone_number=phone_number, code=code)
                redirect_method = 'verification'

            request.session["user_info"] = {
                "email": email,
                "phone_number": phone_number,
                "first_name": first_name,
                "last_name": last_name,
                "verification_method": verification_method,
            }

            CustomUser.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone_number,
            )

            messages.success(
                request,
                "account has been created \n please activate your account with code/token that we sent to you!!",
                "success",
            )
            return redirect(f"accounts:user_{redirect_method}")
        return render(request, "accounts/register.html", {"form": form.errors})


class UserVerificationView(View):
    def get(self, request, *args, **kwargs):
        token = kwargs.get("token")
        if token and request.session.get("verification_method") == "email":
            otp_field = OtpEmail.objects.filter(token=token)
            user_info = request.session.get("user_info")
            user_email = user_info.get("email")
            if otp_field.exists() and user_email == otp_field.first().email:
                pass

            messages.error(request, "invalid token/email !!!")
            return redirect("account:user_register")
        if request.session.get("verification_method") == "phone":
            form = UserVerificationForm()
            return render(
                request, "accounts/verify_user_registration.html", {"form": form}
            )

    def post(self, request, *args, **kwargs):
        pass
