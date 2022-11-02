from django.db import models
from django_extensions.db.models import TimeStampedModel


class PastRandomPhoto(TimeStampedModel):
    image_url = models.CharField(max_length=255)
    item_url = models.CharField(max_length=255)
