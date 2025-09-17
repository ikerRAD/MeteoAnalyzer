from dataclasses import dataclass

from core.domain.models.all_weather_stats_by_city import AllWeatherStatsByCity


@dataclass(frozen=True)
class GetAllWeatherStatsResponse:
    weather_stats_by_city: AllWeatherStatsByCity
