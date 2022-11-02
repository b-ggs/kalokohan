from django.contrib import admin
from solo.admin import SingletonModelAdmin

from .models import Config, PastRandomPhoto

admin.site.register(Config, SingletonModelAdmin)


@admin.register(PastRandomPhoto)
class PastRandomPhotoAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "item_url",
        "created",
    ]
