from typing import cast

from django.db import models
from solo.models import SingletonModel


class Config(SingletonModel):
    api_key = models.CharField(
        max_length=255,
        blank=True,
    )

    def __str__(self):
        return "Config"

    @classmethod
    def get_solo(cls) -> "Config":
        return cast("Config", super().get_solo())

    class Meta:
        verbose_name = "config"
