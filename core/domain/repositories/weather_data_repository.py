from abc import ABC, abstractmethod
from datetime import datetime

from core.domain.models.weather_data import WeatherData


class WeatherDataRepository(ABC):
    @abstractmethod
    def bulk_save(self, weather_data_list: list[WeatherData]) -> None:
        pass

    @abstractmethod
    def get_by_city_id_and_date_range(
        self, city_id: int, start_date: datetime, end_date: datetime
    ) -> list[WeatherData]:
        pass

    @abstractmethod
    def get_by_city_id(self, city_id: int) -> list[WeatherData]:
        pass
