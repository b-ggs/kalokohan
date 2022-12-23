from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from ninja import NinjaAPI

from kalokohan.home import urls as home_urls
from kalokohan.logs.api import router as logs_router
from kalokohan.wallpapers.api import router as wallpapers_router
from kalokohan.weather import urls as weather_urls
from kalokohan.weather.api import prometheus_router as weather_prometheus_router
from kalokohan.weather.renderers import PrometheusMetricsRenderer

api_v1 = NinjaAPI(version="1.0.0", title="Kalokohan JSON API")
api_v1.add_router("logs/", logs_router)
api_v1.add_router("wallpapers/", wallpapers_router)

prometheus_api = NinjaAPI(
    version="1.0.0",
    title="Kalokohan Prometheus API",
    renderer=PrometheusMetricsRenderer(),
    urls_namespace="prometheus-api-1.0.0",
)
prometheus_api.add_router("weather/", weather_prometheus_router)

urlpatterns = [
    path("", include(home_urls)),
    path("django-admin/", admin.site.urls),
    path("api/v1/", api_v1.urls),  # type: ignore
    path("prometheus-api/v1/", prometheus_api.urls),  # type: ignore
    path("weather/", include(weather_urls)),
]

if hasattr(settings, "SENTRY_TEST_URL_ENABLED") and settings.SENTRY_TEST_URL_ENABLED:

    def trigger_error(request):
        return 1 / 0

    urlpatterns += [
        path("_trigger-error/", trigger_error),  # type: ignore
    ]
