from django.contrib import admin

from kalokohan.logs.models import LogItem


@admin.register(LogItem)
class LogItemAdmin(admin.ModelAdmin):
    list_display = [
        "uuid",
        "type",
        "source",
        "message",
        "created",
    ]
    filter_vertial = [
        "type",
        "source",
    ]
