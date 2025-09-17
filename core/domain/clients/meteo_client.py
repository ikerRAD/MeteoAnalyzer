from abc import ABC, abstractmethod

from core.domain.models.city import City
from core.domain.models.weather_data import WeatherData


class MeteoClient(ABC):
    @abstractmethod
    def get_cities_by_name(self, city_name: str) -> list[City]:
        pass

    @abstractmethod
    def get_weather_data_by_city(
        self, city: City, start_date: str, end_date: str
    ) -> list[WeatherData]:
        pass
