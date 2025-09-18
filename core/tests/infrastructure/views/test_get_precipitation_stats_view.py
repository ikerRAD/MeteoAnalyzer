from datetime import datetime, timezone

from django.test import TestCase

from rest_framework.reverse import reverse

from core.infrastructure.persistence.models.django_city import DjangoCity
from core.infrastructure.persistence.models.django_weather_data import DjangoWeatherData


class TestIntegrationGetPrecipitationStatsView(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.madrid_city_1 = DjangoCity.objects.create(
            name="Madrid", latitude=1.0, longitude=1.0, id=1
        )
        cls.weather_data_1 = DjangoWeatherData.objects.create(
            id=1,
            city_id=1,
            date_time=datetime(2010, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
            temperature=10.0,
            precipitation=0.1,
        )
        cls.weather_data_2 = DjangoWeatherData.objects.create(
            id=2,
            city_id=1,
            date_time=datetime(2010, 1, 1, 1, 0, 0, tzinfo=timezone.utc),
            temperature=12.0,
            precipitation=0.2,
        )
        cls.weather_data_3 = DjangoWeatherData.objects.create(
            id=3,
            city_id=1,
            date_time=datetime(2010, 1, 1, 2, 0, 0, tzinfo=timezone.utc),
            temperature=8.0,
            precipitation=0.0,
        )
        cls.madrid_city_1_weather = [
            cls.weather_data_1,
            cls.weather_data_2,
            cls.weather_data_3,
        ]

        cls.madrid_city_2 = DjangoCity.objects.create(
            name="Madrid", latitude=2.0, longitude=2.0, id=2
        )

        cls.madrid_city_3 = DjangoCity.objects.create(
            name="Madrid", latitude=3.0, longitude=3.0, id=3
        )
        cls.weather_data_4 = DjangoWeatherData.objects.create(
            id=4,
            city_id=3,
            date_time=datetime(2010, 1, 6, 0, 0, 0, tzinfo=timezone.utc),
            temperature=5.0,
            precipitation=0.2,
        )
        cls.weather_data_5 = DjangoWeatherData.objects.create(
            id=5,
            city_id=3,
            date_time=datetime(2010, 1, 6, 1, 0, 0, tzinfo=timezone.utc),
            temperature=15.0,
            precipitation=0.0,
        )
        cls.madrid_city_3_weather = [cls.weather_data_4, cls.weather_data_5]

        cls.barcelona_city_1 = DjangoCity.objects.create(
            name="Barcelona", latitude=4.0, longitude=4.0, id=4
        )
        cls.weather_data_6 = DjangoWeatherData.objects.create(
            id=6,
            city_id=4,
            date_time=datetime(2011, 1, 2, 0, 0, 0, tzinfo=timezone.utc),
            temperature=0.0,
            precipitation=0.2,
        )
        cls.weather_data_7 = DjangoWeatherData.objects.create(
            id=7,
            city_id=4,
            date_time=datetime(2011, 1, 2, 1, 0, 0, tzinfo=timezone.utc),
            temperature=10.0,
            precipitation=0.0,
        )
        cls.barcelona_city_1_weather = [cls.weather_data_6, cls.weather_data_7]

        cls.barcelona_city_2 = DjangoCity.objects.create(
            name="Barcelona", latitude=5.0, longitude=5.0, id=5
        )
        cls.weather_data_8 = DjangoWeatherData.objects.create(
            id=8,
            city_id=5,
            date_time=datetime(2010, 2, 2, 0, 0, 0, tzinfo=timezone.utc),
            temperature=5.0,
            precipitation=0.5,
        )
        cls.weather_data_9 = DjangoWeatherData.objects.create(
            id=9,
            city_id=5,
            date_time=datetime(2010, 2, 2, 1, 0, 0, tzinfo=timezone.utc),
            temperature=5.0,
            precipitation=0.0,
        )
        cls.weather_data_10 = DjangoWeatherData.objects.create(
            id=10,
            city_id=5,
            date_time=datetime(2011, 2, 2, 1, 0, 0, tzinfo=timezone.utc),
            temperature=20.0,
            precipitation=1.0,
        )
        cls.barcelona_city_2_weather = [
            cls.weather_data_8,
            cls.weather_data_9,
            cls.weather_data_10,
        ]

    @classmethod
    def tearDownClass(cls):
        [
            weather_data.delete()
            for weather_data in cls.madrid_city_1_weather
            + cls.madrid_city_3_weather
            + cls.barcelona_city_1_weather
            + cls.barcelona_city_2_weather
        ]

        cls.madrid_city_1.delete()
        cls.madrid_city_2.delete()
        cls.madrid_city_3.delete()
        cls.barcelona_city_1.delete()
        cls.barcelona_city_2.delete()

    def test_get(self) -> None:
        url = reverse("precipitation")

        retrieved_response = self.client.get(
            url,
            query_params={
                "city": "Madrid",
                "start_date": "2000-01-01",
                "end_date": "2025-01-01",
            },
        )

        self.assertEqual("/stats/precipitation/", url)
        self.assertEqual(200, retrieved_response.status_code)
        self.assertCountEqual(
            [
                {
                    "latitude": 1.0,
                    "longitude": 1.0,
                    "precipitation": {
                        "total": 0.30000000000000004,
                        "total_by_day": {"2010-01-01": 0.30000000000000004},
                        "days_with_precipitation": 2,
                        "max": {"value": 0.2, "date": "2010-01-01T01:00"},
                        "average": 0.10000000000000002,
                    },
                },
                {
                    "latitude": 3.0,
                    "longitude": 3.0,
                    "precipitation": {
                        "total": 0.2,
                        "total_by_day": {"2010-01-06": 0.2},
                        "days_with_precipitation": 1,
                        "max": {"value": 0.2, "date": "2010-01-06T00:00"},
                        "average": 0.1,
                    },
                },
            ],
            retrieved_response.json(),
        )
