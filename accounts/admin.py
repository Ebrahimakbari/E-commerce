from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from accounts.models import CustomUser, OtpEmail, OtpPhoneNumber
from .forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import Group




@admin.register(OtpPhoneNumber)
class OtpPhoneNumberAdmin(admin.ModelAdmin):
    list_display = ['phone_number', 'code', 'created']


@admin.register(OtpEmail)
class OtpEmailAdmin(admin.ModelAdmin):
    list_display = ['email', 'token', 'created']



@admin.register(CustomUser)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = [
        "first_name",
        "last_name",
        "email",
        "phone_number",
        "is_active",
        "is_admin",
        "date_joined",
        "last_login",
        "avatar",
    ]
    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = ['groups', 'user_permissions']
    list_filter = ["is_admin"]
    fieldsets = [
        (
            None,
            {"fields": ["phone_number", "email", "last_login", "password"]},
        ),
        ("Personal info", {"fields": ["first_name", "last_name", "avatar"]}),
        ("Permissions", {"fields": ["is_admin", "is_active", "is_superuser", "groups", "user_permissions"]}),
    ]
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": [
                    "email",
                    "phone_number",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                ],
            },
        ),
    ]