from django.contrib import admin
from solo.admin import SingletonModelAdmin

from .models import Config

admin.site.register(Config, SingletonModelAdmin)
