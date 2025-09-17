from datetime import datetime, timezone

from django.test import TestCase

from core.domain.models.weather_data import WeatherData
from core.infrastructure.persistence.models.django_city import DjangoCity
from core.infrastructure.persistence.models.django_weather_data import DjangoWeatherData
from core.infrastructure.persistence.repositories.db_weather_data_repository import (
    DbWeatherDataRepository,
)


class TestIntegrationDbWeatherDataRepository(TestCase):
    def setUp(self) -> None:
        self.db_weather_data_repository = DbWeatherDataRepository()

    def test_bulk_save(self) -> None:
        city = DjangoCity.objects.create(
            id=1, name="Nowhere", latitude=0.0, longitude=0.0
        )

        weather_data_list: list[DjangoWeatherData] = list(
            DjangoWeatherData.objects.all()
        )
        self.assertEqual([], weather_data_list)

        domain_weather_data_list = [
            WeatherData(
                city_id=city.id,
                date_time=datetime(2010, 1, 1, tzinfo=timezone.utc),
                precipitation=1.0,
                temperature=30.0,
            ),
            WeatherData(
                city_id=city.id,
                date_time=datetime(2010, 1, 2, tzinfo=timezone.utc),
                precipitation=2.0,
                temperature=31.0,
            ),
        ]

        self.db_weather_data_repository.bulk_save(domain_weather_data_list)

        weather_data_list = list(DjangoWeatherData.objects.all())
        self.assertEqual(2, len(weather_data_list))

        [django_weather_data.delete() for django_weather_data in weather_data_list]
        city.delete()

    def test_bulk_save_ignore_conflicts(self) -> None:
        city = DjangoCity.objects.create(
            id=1, name="Nowhere", latitude=0.0, longitude=0.0
        )

        DjangoWeatherData.objects.create(
            city=city,
            date_time=datetime(2010, 1, 1, tzinfo=timezone.utc),
            precipitation=1.0,
            temperature=30.0,
        )
        weather_data_list: list[DjangoWeatherData] = list(
            DjangoWeatherData.objects.all()
        )
        self.assertEqual(1, len(weather_data_list))
        self.assertEqual(city.id, weather_data_list[0].city_id)
        self.assertEqual(
            datetime(2010, 1, 1, tzinfo=timezone.utc), weather_data_list[0].date_time
        )
        self.assertEqual(1.0, weather_data_list[0].precipitation)
        self.assertEqual(30.0, weather_data_list[0].temperature)

        domain_weather_data_list = [
            WeatherData(
                city_id=city.id,
                date_time=datetime(2010, 1, 1, tzinfo=timezone.utc),
                precipitation=1.0,
                temperature=30.0,
            ),
            WeatherData(
                city_id=city.id,
                date_time=datetime(2010, 1, 2, tzinfo=timezone.utc),
                precipitation=2.0,
                temperature=31.0,
            ),
        ]

        self.db_weather_data_repository.bulk_save(domain_weather_data_list)

        weather_data_list = list(DjangoWeatherData.objects.all())
        self.assertEqual(2, len(weather_data_list))

        [django_weather_data.delete() for django_weather_data in weather_data_list]
        city.delete()
