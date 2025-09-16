from django.urls import path, reverse_lazy
from django.views.generic import RedirectView

from core.views import schema_view

urlpatterns = [
    path("", RedirectView.as_view(url=reverse_lazy("docs"), permanent=True)),
    path("docs/", schema_view.with_ui("swagger", cache_timeout=0), name="docs"),
]
