from datetime import datetime
from dataclasses import dataclass

from core.domain.models.city import City


@dataclass
class WeatherData:
    city: City
    date_time: datetime
    temperature: float
    precipitation: float
    id: int | None = None

    def __str__(self):
        return f"{self.city.name} - {self.date_time.strftime('%Y-%m-%d %H:%M')}"
