from datetime import datetime
from dataclasses import dataclass


@dataclass
class WeatherData:
    city_id: int
    date_time: datetime
    temperature: float
    precipitation: float
    id: int | None = None
