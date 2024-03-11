from typing import cast

from django.db import models
from solo.models import SingletonModel


class WeightItem(models.Model):
    weight_lbs = models.DecimalField(max_digits=5, decimal_places=2)
    weighed_at = models.DateField()

    def __str__(self) -> str:
        return f"{self.weighed_at} - {self.weight_lbs} lbs"

    class Meta:  # pyright: ignore [reportIncompatibleVariableOverride]
        ordering = ["-weighed_at"]


class APIConfiguration(SingletonModel):
    api_key = models.CharField(max_length=255, blank=True)

    def __str__(self) -> str:
        return "API Configuration"

    @classmethod
    def get_solo(cls) -> "APIConfiguration":
        return cast("APIConfiguration", super().get_solo())

    class Meta:  # pyright: ignore [reportIncompatibleVariableOverride]
        verbose_name = "API configuration"
