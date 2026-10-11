import uuid

from django.conf import settings

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models.functions import Lower

from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model for FixBase

    Authentication identifier:
        email
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name=_('ID'))

    email = models.EmailField(unique=True, verbose_name=_('Email'))
    
    first_name = models.CharField(max_length=150, blank=True, verbose_name=_('First Name'))
    last_name = models.CharField(max_length=150, blank=True, verbose_name=_('Last Name'))

    is_active = models.BooleanField(default=True, verbose_name=_('Is Active'))
    is_staff = models.BooleanField(default=False, verbose_name=_('Is Admin'))
    
    is_email_verified = models.BooleanField(default=False,verbose_name=_('Is email Verified'))
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name=_('Data joined'))

    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ["-date_joined"]
        constraints = [
            models.UniqueConstraint(Lower("email"), name="accounts_user_email_ci")
        ]

    def clean(self):
        super().clean()
        self.email = type(self).objects.normalize_email(self.email)
    
    def save(self, *args, **kwargs):
        self.email = type(self).objects.normalize_email(self.email)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        return self.first_name or self.email



class Profile(BaseModel):
    """
    Additional optional information for a user.
    """
    PAGE_SIZES = (10, 20, 50, 100, 200)

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="User",
    )

    avatar = models.ImageField(
        upload_to="avatars/%Y/%m/",
        blank=True, null=True,
        verbose_name="Profile picture",
    )

    bio = models.TextField(
        blank=True,
        verbose_name="Bio",
    )
    
    default_page_size = models.PositiveBigIntegerField(
        default=20, 
        choices=[(size, str(size)) for size in PAGE_SIZES]

    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                condition=models.Q(
                    default_page_size__in=[10, 20, 50, 100, 200],
                    name="accounts_profile_page_size_valid",
                )
            )
        ]
    def __str__(self):
        return f"Profile: {self.user.email}"