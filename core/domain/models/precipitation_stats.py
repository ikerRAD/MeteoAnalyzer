from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class PrecipitationStats:
    total: float
    total_by_day: dict[str, float]
    days_with_precipitation: int
    max: dict[str, float | str]
    average: float

    def to_dict(self) -> dict[str, Any]:
        return {
            "total": float(self.total),
            "total_by_day": {
                key: float(value) for key, value in self.total_by_day.items()
            },
            "days_with_precipitation": int(self.days_with_precipitation),
            "max": {
                "value": float(self.max["precipitation"]),
                "date": self.max["date_time"],
            },
            "average": float(self.average),
        }
