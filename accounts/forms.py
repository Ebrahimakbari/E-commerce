from django import forms
from .models import CustomUser
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.db.models import Q
from django.core.exceptions import ValidationError


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password", widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = CustomUser
        fields = [
            "email",
            "phone_number",
            "first_name",
            "last_name",
        ]
        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
        }
        labels = {
            "email": "Email",
            "phone_number": "Phone Number",
            "first_name": "First Name",
            "last_name": "Last Name",
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password2 != password1:
            raise forms.ValidationError("Mismatch passwords!!")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get("password2"))
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        help_text='you can change password using this <a href="../password/">form</a>'
    )
    date_joined = forms.CharField(disabled=True, required=False)

    class Meta:
        model = CustomUser
        exclude = ["date_joined"]


class UserRegistrationForm(forms.Form):
    VERIFICATION_CHOICES = [
        ("email", "Email Verification"),
        ("phone", "Phone Number Verification"),
    ]

    phone_number = forms.CharField(
        label="Phone Number", widget=forms.TextInput(attrs={"class": "form-control"})
    )
    email = forms.EmailField(
        label="Email", widget=forms.EmailInput(attrs={"class": "form-control"})
    )
    first_name = forms.CharField(
        label="First Name", widget=forms.TextInput(attrs={"class": "form-control"})
    )
    last_name = forms.CharField(
        label="Last Name", widget=forms.TextInput(attrs={"class": "form-control"})
    )
    password = forms.CharField(
        label="Password", widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    verification_method = forms.ChoiceField(
        label="Select Verification Method",
        choices=VERIFICATION_CHOICES,
        widget=forms.RadioSelect,
    )

    def clean(self):
        validate_data = super().clean()
        phone_number = validate_data.get("phone_number")
        email = validate_data.get("email")
        users = CustomUser.objects.filter(Q(phone_number=phone_number) | Q(email=email))
        if users.exists():
            raise ValidationError("Email or Phone number is already signed up!!!")


class UserVerificationForm(forms.Form):
    code = forms.CharField(
        max_length=4,
        label="Code",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )


class UserLoginForm(forms.Form):
    phone_number = forms.CharField(
        max_length=11,
        label="Phone Number",
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    password = forms.CharField(
        label="Password", widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        user = CustomUser.objects.filter(phone_number=phone_number)
        if not (user.exists() and user.first().phone_number == phone_number):
            raise ValidationError("user with given phone number not found!!")
        return phone_number


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["email", "phone_number", "first_name", "last_name",  "avatar"]
        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            # "avatar": forms.FileInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field_name in ["email", "phone_number"]:
            self.fields[field_name].disabled = True