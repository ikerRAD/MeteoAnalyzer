from dataclasses import dataclass

from core.domain.models.city_precipitation_stats import CityPrecipitationStats


@dataclass(frozen=True)
class GetPrecipitationStatsResponse:
    precipitation_stats_for_cities: list[CityPrecipitationStats]
