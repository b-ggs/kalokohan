from django.contrib import admin

from .models import PastRandomPhoto


@admin.register(PastRandomPhoto)
class PastRandomPhotoAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "item_url",
        "created",
    ]
