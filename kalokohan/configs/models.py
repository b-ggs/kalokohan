from typing import cast

from django.db import models
from solo.models import SingletonModel


class SiteConfiguration(SingletonModel):
    api_key = models.CharField(
        max_length=255,
        blank=True,
    )

    def __str__(self):
        return "Site Configuration"

    @classmethod
    def get_solo(cls) -> "SiteConfiguration":
        return cast("SiteConfiguration", super().get_solo())

    class Meta:  # pyright: ignore [reportIncompatibleVariableOverride]
        verbose_name = "Site Configuration"
