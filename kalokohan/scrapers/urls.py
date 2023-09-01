from django.urls import path

from . import views

urlpatterns = [
    path(
        "cg-pinned-post/",
        views.CGPinnedPostView.as_view(),
        name="cg_pinned_post",
    ),
]
