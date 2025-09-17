from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class StatsQuery:
    city_name: str
    start_date: datetime
    end_date: datetime
    latitude: float | None
    longitude: float | None
    upper_threshold: float
    lower_threshold: float
