from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any

from core.domain.models.city_weather_stats import CityWeatherStats


@dataclass(frozen=True)
class AllWeatherStatsByCity:
    all_city_weather_stats: defaultdict[str, list[CityWeatherStats]] = field(
        default_factory=lambda: defaultdict(list)
    )

    def to_dict(self) -> dict[str, list[Any]]:
        return {
            key: [city_value.to_dict() for city_value in value]
            for key, value in self.all_city_weather_stats.items()
        }
