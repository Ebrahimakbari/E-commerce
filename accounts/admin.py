from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from accounts.models import CustomUser
from .forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import Group


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
        "token",
        "avatar",
    ]
    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = []
    list_filter = ["is_admin"]
    fieldsets = [
        (
            None,
            {"fields": ["phone_number", "email", "last_login", "token", "password"]},
        ),
        ("Personal info", {"fields": ["first_name", "last_name", "avatar"]}),
        ("Permissions", {"fields": ["is_admin", "is_active"]}),
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


admin.site.unregister(Group)
