from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from ninja import NinjaAPI

from kalokohan.home import urls as home_urls
from kalokohan.logs.api import router as logs_router

api_v1 = NinjaAPI(version="1.0.0")
api_v1.add_router("logs/", logs_router)

urlpatterns = [
    path("", include(home_urls)),
    path("django-admin/", admin.site.urls),
    path("api/v1/", api_v1.urls),  # type: ignore
]

if hasattr(settings, "SENTRY_TEST_URL_ENABLED") and settings.SENTRY_TEST_URL_ENABLED:

    def trigger_error(request):
        return 1 / 0

    urlpatterns += [
        path("_trigger-error/", trigger_error),
    ]
