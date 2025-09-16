from core.domain.models.weather_data import WeatherData
from core.domain.repositories.weather_data_repository import WeatherDataRepository
from core.infrastructure.persistence.models.django_weather_data import DjangoWeatherData


class DbWeatherDataRepository(WeatherDataRepository):
    def __init__(self):
        self.__django_weather_data_manager = DjangoWeatherData.objects

    def bulk_save(self, weather_data_list: list[WeatherData]) -> list[WeatherData]:
        django_weather_data_list = [
            DjangoWeatherData.from_domain(weather_data)
            for weather_data in weather_data_list
        ]

        saved_instances = self.__django_weather_data_manager.bulk_create(
            django_weather_data_list
        )

        return [instance.to_domain() for instance in saved_instances]
