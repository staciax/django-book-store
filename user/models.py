from typing import Any, ClassVar, Self

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.db.models.functions import Now

# https://docs.djangoproject.com/en/5.0/topics/auth/customizing/#a-full-example


class CustomUserManager[T: 'User'](BaseUserManager[T]):
    def create_user(self, email: str, password: str, **extra_fields: Any) -> Any:
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: str, **extra_fields: Any) -> Any:
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=128, default='', blank=True)
    last_name = models.CharField(max_length=128, default='', blank=True)
    email = models.EmailField(max_length=255, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    phone_number = models.CharField(
        max_length=10,
        default='',
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, db_default=Now())
    updated_at = models.DateTimeField(auto_now=True, db_default=Now())

    objects: ClassVar[CustomUserManager[Self]] = CustomUserManager()  # type: ignore[assignment]

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # noqa: RUF012

    def __str__(self) -> str:
        return self.email

    @property
    def is_customer(self) -> bool:
        return not self.is_staff and not self.is_superuser

    class Meta:
        db_table = 'users'
        verbose_name = 'user'
        verbose_name_plural = 'users'
        abstract = False

    # https://github.com/django/django/blob/222bf2932b55ebc964ffc5f9a6f47bad083e5ac2/django/contrib/auth/models.py#L385

    def clean(self) -> None:
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self) -> str:
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = f'{self.first_name} {self.last_name}'
        return full_name.strip()

    def get_short_name(self) -> str:
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject: str, message: str, from_email: str | None = None, **kwargs: Any) -> None:
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    # -
