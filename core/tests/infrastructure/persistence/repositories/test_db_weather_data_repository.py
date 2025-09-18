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

    def test_get_by_city_id_and_date_range(self) -> None:
        city_1 = DjangoCity.objects.create(
            id=1, name="Nowhere", latitude=0.0, longitude=0.0
        )
        city_2 = DjangoCity.objects.create(
            id=2, name="Somewhere", latitude=1.0, longitude=10.4
        )

        weather_data_1 = DjangoWeatherData.objects.create(
            id=1,
            city_id=1,
            date_time=datetime(2010, 1, 1, 0, 0, tzinfo=timezone.utc),
            temperature=15.6,
            precipitation=0.0,
        )
        weather_data_2 = DjangoWeatherData.objects.create(
            id=2,
            city_id=1,
            date_time=datetime(2010, 2, 1, 0, 0, tzinfo=timezone.utc),
            temperature=15.4,
            precipitation=0.0,
        )
        weather_data_3 = DjangoWeatherData.objects.create(
            id=3,
            city_id=1,
            date_time=datetime(2010, 2, 1, 1, 0, tzinfo=timezone.utc),
            temperature=15.0,
            precipitation=0.01,
        )
        weather_data_4 = DjangoWeatherData.objects.create(
            id=4,
            city_id=1,
            date_time=datetime(2010, 2, 1, 2, 0, tzinfo=timezone.utc),
            temperature=14.6,
            precipitation=0.0,
        )
        weather_data_5 = DjangoWeatherData.objects.create(
            id=5,
            city_id=1,
            date_time=datetime(2010, 3, 2, 0, 0, tzinfo=timezone.utc),
            temperature=15.2,
            precipitation=0.0,
        )
        weather_data_6 = DjangoWeatherData.objects.create(
            id=6,
            city_id=2,
            date_time=datetime(2010, 2, 1, 0, 0, tzinfo=timezone.utc),
            temperature=17.6,
            precipitation=0.0,
        )

        retrieved_weather_data_1 = (
            self.db_weather_data_repository.get_by_city_id_and_date_range(
                1,
                datetime(2010, 2, 1, 0, 0, tzinfo=timezone.utc),
                datetime(2010, 3, 1, 0, 0, tzinfo=timezone.utc),
            )
        )
        retrieved_weather_data_2 = (
            self.db_weather_data_repository.get_by_city_id_and_date_range(
                2,
                datetime(2010, 2, 1, 0, 0, tzinfo=timezone.utc),
                datetime(2010, 3, 1, 0, 0, tzinfo=timezone.utc),
            )
        )

        self.assertEqual(3, len(retrieved_weather_data_1))
        self.assertCountEqual(
            [
                weather_data_2.to_domain(),
                weather_data_3.to_domain(),
                weather_data_4.to_domain(),
            ],
            retrieved_weather_data_1,
        )

        self.assertEqual(1, len(retrieved_weather_data_2))
        self.assertEqual([weather_data_6.to_domain()], retrieved_weather_data_2)

        weather_data_1.delete()
        weather_data_2.delete()
        weather_data_3.delete()
        weather_data_4.delete()
        weather_data_5.delete()
        weather_data_6.delete()

        city_1.delete()
        city_2.delete()

    def test_get_by_city_id(self) -> None:
        city_1 = DjangoCity.objects.create(
            id=1, name="Nowhere", latitude=0.0, longitude=0.0
        )
        city_2 = DjangoCity.objects.create(
            id=2, name="Somewhere", latitude=1.0, longitude=10.4
        )

        weather_data_1 = DjangoWeatherData.objects.create(
            id=1,
            city_id=1,
            date_time=datetime(2010, 1, 1, 0, 0, tzinfo=timezone.utc),
            temperature=15.6,
            precipitation=0.0,
        )
        weather_data_2 = DjangoWeatherData.objects.create(
            id=2,
            city_id=1,
            date_time=datetime(2010, 2, 1, 0, 0, tzinfo=timezone.utc),
            temperature=15.4,
            precipitation=0.0,
        )
        weather_data_3 = DjangoWeatherData.objects.create(
            id=3,
            city_id=1,
            date_time=datetime(2010, 2, 1, 1, 0, tzinfo=timezone.utc),
            temperature=15.0,
            precipitation=0.01,
        )
        weather_data_4 = DjangoWeatherData.objects.create(
            id=4,
            city_id=1,
            date_time=datetime(2010, 2, 1, 2, 0, tzinfo=timezone.utc),
            temperature=14.6,
            precipitation=0.0,
        )
        weather_data_5 = DjangoWeatherData.objects.create(
            id=5,
            city_id=1,
            date_time=datetime(2010, 3, 2, 0, 0, tzinfo=timezone.utc),
            temperature=15.2,
            precipitation=0.0,
        )
        weather_data_6 = DjangoWeatherData.objects.create(
            id=6,
            city_id=2,
            date_time=datetime(2010, 2, 1, 0, 0, tzinfo=timezone.utc),
            temperature=17.6,
            precipitation=0.0,
        )

        retrieved_weather_data_1 = self.db_weather_data_repository.get_by_city_id(1)
        retrieved_weather_data_2 = self.db_weather_data_repository.get_by_city_id(2)

        self.assertEqual(5, len(retrieved_weather_data_1))
        self.assertCountEqual(
            [
                weather_data_1.to_domain(),
                weather_data_2.to_domain(),
                weather_data_3.to_domain(),
                weather_data_4.to_domain(),
                weather_data_5.to_domain(),
            ],
            retrieved_weather_data_1,
        )

        self.assertEqual(1, len(retrieved_weather_data_2))
        self.assertEqual([weather_data_6.to_domain()], retrieved_weather_data_2)

        weather_data_1.delete()
        weather_data_2.delete()
        weather_data_3.delete()
        weather_data_4.delete()
        weather_data_5.delete()
        weather_data_6.delete()

        city_1.delete()
        city_2.delete()
