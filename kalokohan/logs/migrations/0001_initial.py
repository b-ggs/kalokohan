# Generated by Django 3.2.16 on 2022-10-27 16:47

import uuid

import django_extensions.db.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="LogItem",
            fields=[
                (
                    "created",
                    django_extensions.db.fields.CreationDateTimeField(
                        auto_now_add=True, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    django_extensions.db.fields.ModificationDateTimeField(
                        auto_now=True, verbose_name="modified"
                    ),
                ),
                (
                    "uuid",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[("WALLPAPER", "wallpaper")], max_length=32
                    ),
                ),
                (
                    "source",
                    models.CharField(
                        choices=[("APPLE_SHORTCUTS", "apple shortcuts")], max_length=32
                    ),
                ),
                ("message", models.TextField(blank=True)),
            ],
            options={
                "get_latest_by": "modified",
                "abstract": False,
            },
        ),
    ]
