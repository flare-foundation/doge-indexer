from string import ascii_lowercase, ascii_uppercase, digits, punctuation

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core import exceptions
from django.db import models
from simple_history.models import HistoricalRecords


class AFPasswordValidator:
    def __init__(self):
        pass

    def validate(self, password, user=None):
        length = False
        upper = False
        lower = False
        digit = False
        special = False

        if len(password) >= 9:
            length = True

        for c in password:
            if c in ascii_uppercase:
                upper = True
            elif c in ascii_lowercase:
                lower = True
            elif c in digits:
                digit = True
            elif c in punctuation:
                special = True

        if not (length and upper and lower and digit and special):
            raise exceptions.ValidationError(
                "Password must contain at least 9 characters, one uppercase letter, "
                "one lowercase letter, one digit and one special character",
                code="password_too_weak",
            )

    def get_help_text(self):
        return "Password must contain at least 9 characters, one uppercase letter, one lowercase letter, one digit and one special character"


class UserManager(BaseUserManager["AFUser"]):
    use_in_migrations = True

    def create_user(
        self, email: str, first_name: str, last_name: str, password: str | None = None, is_active: bool = True, **kwargs
    ) -> "AFUser":
        """
        Creates and saves a User with the given email, first_name, last_name
        and password
        """
        if not email:
            raise ValueError("Users must have an email address")

        if "username" in kwargs:
            kwargs.pop("username")

        user = self.model(
            email=self.normalize_email(email),
            username=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            is_active=is_active,
            **kwargs,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email: str, first_name: str, last_name: str, password: str | None, **kwargs) -> "AFUser":
        """
        Creates and saves a superuser with the given email, first_name,
        last_name and password
        """
        user = self.create_user(email=email, password=password, first_name=first_name, last_name=last_name, **kwargs)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class AFUser(AbstractUser):
    """
    Core user object
    """

    # we want email as username field and username field has to be unique
    email = models.EmailField(max_length=255, unique=True)

    history = HistoricalRecords()

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("username", "first_name", "last_name")

    class Meta:
        verbose_name = "uporabnik"
        verbose_name_plural = "uporabniki"
        ordering = ("email",)

    #################################################################
    # Pretty printing

    def __str__(self) -> str:
        return self.get_full_name()

    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
