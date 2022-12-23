from django.urls import path

from . import views

urlpatterns = [
    path("metrics/", views.MetricsView.as_view()),
]
