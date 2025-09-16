from abc import ABC, abstractmethod

from core.domain.models.weather_data import WeatherData


class WeatherDataRepository(ABC):
    @abstractmethod
    def bulk_save(self, weather_data_list: list[WeatherData]) -> list[WeatherData]:
        pass
