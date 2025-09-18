from dataclasses import dataclass
from typing import Any

from core.domain.models.temperature_stats import TemperatureStats


@dataclass(frozen=True)
class CityTemperatureStats:
    latitude: float
    longitude: float
    temperature_stats: TemperatureStats

    def to_dict(self) -> dict[str, Any]:
        return {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "temperature": self.temperature_stats.to_dict(),
        }
