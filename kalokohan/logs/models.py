import uuid
from typing import Literal

from django.db import models
from django_extensions.db.models import TimeStampedModel


class LogType(models.TextChoices):
    WALLPAPER = "WALLPAPER", "wallpaper"


LogTypeType = Literal[
    "WALLPAPER",
]


class LogSource(models.TextChoices):
    APPLE_SHORTCUTS = "APPLE_SHORTCUTS", "apple shortcuts"


LogSourceType = Literal[
    "APPLE_SHORTCUTS",
]


class LogItem(TimeStampedModel):
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
    )
    log_type = models.CharField(
        max_length=32,
        choices=LogType.choices,
    )
    log_source = models.CharField(
        max_length=32,
        choices=LogSource.choices,
    )
    message = models.TextField(blank=True)
