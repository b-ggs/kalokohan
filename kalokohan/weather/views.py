from django.http import HttpRequest
from django.http.response import HttpResponse
from django.views.generic import View
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from kalokohan.weather.clients import get_open_meteo_client


class MetricsView(View):
    def get(
        self,
        request: HttpRequest,
        *args,
        **kwargs,
    ) -> HttpResponse:
        x = get_open_meteo_client()

        breakpoint()

        return HttpResponse(
            generate_latest(),
            content_type=CONTENT_TYPE_LATEST,
        )
