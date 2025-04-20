from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(
        self, phone_number, email, first_name, last_name, password, **extra_fields
    ):
        if not phone_number:
            raise ValueError("The given phone_number must be set")
        if not email:
            raise ValueError("The given email must be set")
        if not first_name:
            raise ValueError("The given first_name must be set")
        if not last_name:
            raise ValueError("The given last_name must be set")

        email = self.normalize_email(email)
        user = self.model(
            phone_number=phone_number,
            email=email,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, phone_number, email, first_name, last_name, password, **extra_fields
    ):
        user = self.create_user(
            phone_number, email, first_name, last_name, password, **extra_fields
        )
        user.is_admin = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
