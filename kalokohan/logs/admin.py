from django.contrib import admin

from kalokohan.logs.models import LogItem


@admin.register(LogItem)
class LogItemAdmin(admin.ModelAdmin):
    list_display = [
        "uuid",
        "log_type",
        "log_source",
        "message",
        "created",
    ]
    list_filter = [
        "log_type",
        "log_source",
    ]
