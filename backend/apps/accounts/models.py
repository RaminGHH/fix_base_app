import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from core.models import BaseModel

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model for FixBase.

    Authentication identifier:
        email
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    email = models.EmailField(
        unique=True,
        verbose_name="ایمیل",
    )

    first_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="نام",
    )

    last_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="نام خانوادگی",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="فعال",
    )

    is_staff = models.BooleanField(
        default=False,
        verbose_name="کارمند",
    )

    is_email_verified = models.BooleanField(
        default=False,
        verbose_name="ایمیل تأیید شده",
    )

    date_joined = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ عضویت",
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"
        ordering = ["-date_joined"]

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        return self.first_name


class Profile(BaseModel):
    """
    Additional optional information for a user.
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="کاربر",
    )

    avatar = models.ImageField(
        upload_to="avatars/%Y/%m/",
        blank=True,
        null=True,
        verbose_name="تصویر پروفایل",
    )

    bio = models.TextField(
        blank=True,
        verbose_name="درباره من",
    )

    def __str__(self):
        return f"Profile: {self.user.email}"