from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class CityWeatherStats:
    latitude: float
    longitude: float
    start_date: str
    end_date: str
    temperature_average: float
    precipitation_total: float
    days_with_precipitation: int
    precipitation_max: dict[str, float | str]
    temperature_max: dict[str, float | str]
    temperature_min: dict[str, float | str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "temperature_average": float(self.temperature_average),
            "precipitation_total": float(self.precipitation_total),
            "days_with_precipitation": int(self.days_with_precipitation),
            "precipitation_max": {
                "date": self.precipitation_max["date_time"],
                "value": self.precipitation_max["precipitation"],
            },
            "temperature_max": {
                "date": self.temperature_max["date_time"],
                "value": self.temperature_max["temperature"],
            },
            "temperature_min": {
                "date": self.temperature_min["date_time"],
                "value": self.temperature_min["temperature"],
            },
        }
