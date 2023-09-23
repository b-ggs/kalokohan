from django.contrib import admin
from solo.admin import SingletonModelAdmin

from .models import APIConfiguration, WeightItem

admin.site.register(WeightItem)
admin.site.register(APIConfiguration, SingletonModelAdmin)
