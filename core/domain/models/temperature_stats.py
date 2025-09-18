from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class TemperatureStats:
    average: float
    average_by_day: dict[str, float]
    max: dict[str, float | str]
    min: dict[str, float]
    hours_above_threshold: int
    hours_below_threshold: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "average": float(self.average),
            "average_by_day": {
                key: float(value) for key, value in self.average_by_day.items()
            },
            "max": {
                "value": float(self.max["temperature"]),
                "date": self.max["date_time"],
            },
            "min": {
                "value": float(self.min["temperature"]),
                "date": self.min["date_time"],
            },
            "hours_above_threshold": int(self.hours_above_threshold),
            "hours_below_threshold": int(self.hours_below_threshold),
        }
