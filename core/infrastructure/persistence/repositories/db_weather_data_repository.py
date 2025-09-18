from datetime import datetime

from core.domain.models.weather_data import WeatherData
from core.domain.repositories.weather_data_repository import WeatherDataRepository
from core.infrastructure.persistence.models.django_weather_data import DjangoWeatherData


class DbWeatherDataRepository(WeatherDataRepository):
    def __init__(self):
        self.__django_weather_data_manager = DjangoWeatherData.objects

    def bulk_save(self, weather_data_list: list[WeatherData]) -> None:
        django_weather_data_list = [
            DjangoWeatherData.from_domain(weather_data)
            for weather_data in weather_data_list
        ]

        self.__django_weather_data_manager.bulk_create(
            django_weather_data_list, ignore_conflicts=True
        )

    def get_by_city_id_and_date_range(
        self, city_id: int, start_date: datetime, end_date: datetime
    ) -> list[WeatherData]:
        django_weather_data_query_set = self.__django_weather_data_manager.filter(
            city_id=city_id, date_time__gte=start_date, date_time__lte=end_date
        )

        return [
            django_weather_data.to_domain()
            for django_weather_data in django_weather_data_query_set
        ]

    def get_by_city_id(self, city_id: int) -> list[WeatherData]:
        return [
            django_weather_data.to_domain()
            for django_weather_data in self.__django_weather_data_manager.filter(
                city_id=city_id
            )
        ]
