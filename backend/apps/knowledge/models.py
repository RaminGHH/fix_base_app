from django.conf import settings
from django.core.validators import MaxLengthValidator, URLValidator
from django.db import models
from django.db.models.functions import Lower

from core.models import BaseModel


class Tag(BaseModel):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="knowledge_tags",
    )
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ("name", "id")
        constraints = [
            models.UniqueConstraint(
                Lower("name"), "owner",
                name="knowledge_tag_owner_name_ci",
            ),
        ]

    def __str__(self) -> str:
        return self.name


class Entry(BaseModel):
    class Kind(models.TextChoices):
        SNIPPET = "snippet", "قطعه‌کد"
        COMMAND = "command", "کامند"
        SOLUTION = "solution", "راه‌حل"
        NOTE = "note", "یادداشت"

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="knowledge_entries",
    )
    title = models.CharField(max_length=200)
    kind = models.CharField(
        max_length=16,
        choices=Kind.choices,
        default=Kind.NOTE,
    )
    problem = models.TextField(
        blank=True,
        validators=[MaxLengthValidator(50_000)],
    )
    content = models.TextField(
        validators=[MaxLengthValidator(200_000)],
        help_text="متن خام یا Markdown؛ کد در سرور اجرا نمی‌شود.",
    )
    environment = models.CharField(max_length=255, blank=True)
    source_url = models.URLField(
        max_length=2000,
        blank=True,
        validators=[URLValidator(schemes=["http", "https"])],
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="entries",
    )
    is_favorite = models.BooleanField(default=False)

    class Meta:
        ordering = ("-created_at", "-id")
        indexes = [
            models.Index(
                fields=["owner", "-created_at", "-id"],
                name="knowledge_owner_created_idx",
            ),
            models.Index(
                fields=["owner", "kind"],
                name="knowledge_owner_kind_idx",
            ),
        ]

    def __str__(self) -> str:
        return self.title