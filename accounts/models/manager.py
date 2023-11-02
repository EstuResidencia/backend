from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):

    def create_user(self, correo, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """

        if not correo:
            raise ValueError(_("The email must be set"))

        user = self.model(correo=correo, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, correo, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("validado", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))

        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(correo, password, **extra_fields)