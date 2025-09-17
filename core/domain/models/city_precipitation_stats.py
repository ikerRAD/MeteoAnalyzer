from dataclasses import dataclass
from typing import Any

from core.domain.models.precipitation_stats import PrecipitationStats


@dataclass(frozen=True)
class CityPrecipitationStats:
    latitude: float
    longitude: float
    precipitation_stats: PrecipitationStats

    def to_dict(self) -> dict[str, Any]:
        return {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "precipitation": self.precipitation_stats.to_dict(),
        }
