from dataclasses import dataclass

from core.domain.models.city_temperature_stats import CityTemperatureStats


@dataclass(frozen=True)
class GetTemperatureStatsResponse:
    temperature_stats_for_cities: list[CityTemperatureStats]
