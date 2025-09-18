from django.urls import path, reverse_lazy
from django.views.generic import RedirectView

from core.infrastructure.views.get_all_weather_stats_view import GetAllWeatherStatsView
from core.infrastructure.views.get_precipitation_stats_view import (
    GetPrecipitationStatsView,
)
from core.infrastructure.views.get_temperature_stats_view import GetTemperatureStatsView
from core.views import schema_view

urlpatterns = [
    path("", RedirectView.as_view(url=reverse_lazy("docs"), permanent=True)),
    path("docs/", schema_view.with_ui("swagger", cache_timeout=0), name="docs"),
    path("stats/temperature/", GetTemperatureStatsView.as_view(), name="temperature"),
    path(
        "stats/precipitation/",
        GetPrecipitationStatsView.as_view(),
        name="precipitation",
    ),
    path("stats/all/", GetAllWeatherStatsView.as_view(), name="all"),
]
