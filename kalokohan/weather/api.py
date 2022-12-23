from django.http import HttpRequest
from ninja import Router

prometheus_router = Router()


@prometheus_router.get("/metrics/")
def metrics(request: HttpRequest) -> bytes:
    return "test from view".encode("utf-8")
