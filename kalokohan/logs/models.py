import uuid
from typing import Literal

from django.db import models
from django_extensions.db.models import TimeStampedModel


class LogItemType(models.TextChoices):
    WALLPAPER = "WALLPAPER", "wallpaper"


LogItemTypeType = Literal[
    "WALLPAPER",
]


class LogItemSource(models.TextChoices):
    APPLE_SHORTCUTS = "APPLE_SHORTCUTS", "apple shortcuts"


LogItemSourceType = Literal[
    "APPLE_SHORTCUTS",
]


class LogItem(TimeStampedModel):
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
    )
    type = models.CharField(
        max_length=32,
        choices=LogItemType.choices,
    )
    source = models.CharField(
        max_length=32,
        choices=LogItemSource.choices,
    )
    message = models.TextField(blank=True)
