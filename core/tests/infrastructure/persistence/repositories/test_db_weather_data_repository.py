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

    def test_save(self) -> None:
        city = DjangoCity.objects.create(
            id=1, name="Nowhere", latitude=0.0, longitude=0.0
        )

        weather_data_list: list[DjangoWeatherData] = list(
            DjangoWeatherData.objects.all()
        )
        self.assertEqual([], weather_data_list)

        domain_weather_data_list = [
            WeatherData(
                city=city.to_domain(),
                date_time=datetime(2010, 1, 1, tzinfo=timezone.utc),
                precipitation=1.0,
                temperature=30.0,
            ),
            WeatherData(
                city=city.to_domain(),
                date_time=datetime(2010, 1, 2, tzinfo=timezone.utc),
                precipitation=2.0,
                temperature=31.0,
            ),
        ]

        domain_weather_data = self.db_weather_data_repository.bulk_save(
            domain_weather_data_list
        )

        weather_data_list = list(DjangoWeatherData.objects.all())
        self.assertEqual(2, len(weather_data_list))

        weather_data = weather_data_list[0]
        self.assertEqual(city.id, weather_data.city_id)
        self.assertEqual(
            datetime(2010, 1, 1, tzinfo=timezone.utc), weather_data.date_time
        )
        self.assertEqual(1.0, weather_data.precipitation)
        self.assertEqual(30.0, weather_data.temperature)

        weather_data = weather_data_list[1]
        self.assertEqual(city.id, weather_data.city_id)
        self.assertEqual(
            datetime(2010, 1, 2, tzinfo=timezone.utc), weather_data.date_time
        )
        self.assertEqual(2.0, weather_data.precipitation)
        self.assertEqual(31.0, weather_data.temperature)

        self.assertCountEqual(
            domain_weather_data,
            [weather_data_dom.to_domain() for weather_data_dom in weather_data_list],
        )

        [django_weather_data.delete() for django_weather_data in weather_data_list]
        city.delete()
