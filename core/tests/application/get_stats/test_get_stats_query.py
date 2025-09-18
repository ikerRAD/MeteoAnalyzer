from datetime import datetime
from unittest import TestCase
from unittest.mock import Mock, call

from core.application.get_stats.get_stats_query import GetStatsQuery
from core.domain.models.city import City
from core.domain.models.city_precipitation_stats import CityPrecipitationStats
from core.domain.models.city_temperature_stats import CityTemperatureStats
from core.domain.models.precipitation_stats import PrecipitationStats
from core.domain.models.stats_query import StatsQuery
from core.domain.models.temperature_stats import TemperatureStats
from core.domain.models.weather_data import WeatherData
from core.domain.repositories.city_repository import CityRepository
from core.domain.repositories.weather_data_repository import WeatherDataRepository


class TestGetStatsQuery(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.madrid_city_1 = City("Madrid", 1.0, 1.0, id=1)
        cls.weather_data_1 = WeatherData(1, datetime(2010, 1, 1, 0, 0, 0), 10.0, 0.1)
        cls.weather_data_2 = WeatherData(1, datetime(2010, 1, 1, 1, 0, 0), 12.0, 0.2)
        cls.weather_data_3 = WeatherData(1, datetime(2010, 1, 1, 2, 0, 0), 8.0, 0.0)
        cls.madrid_city_1_weather = [
            cls.weather_data_1,
            cls.weather_data_2,
            cls.weather_data_3,
        ]

        cls.madrid_city_2 = City("Madrid", 2.0, 2.0, id=2)

        cls.madrid_city_3 = City("Madrid", 3.0, 3.0, id=3)
        cls.weather_data_4 = WeatherData(3, datetime(2010, 1, 6, 0, 0, 0), 5.0, 0.2)
        cls.weather_data_5 = WeatherData(3, datetime(2010, 1, 6, 1, 0, 0), 15.0, 0.0)
        cls.madrid_city_3_weather = [cls.weather_data_4, cls.weather_data_5]

        cls.barcelona_city_1 = City("Barcelona", 4.0, 4.0, id=4)
        cls.weather_data_6 = WeatherData(4, datetime(2011, 1, 2, 0, 0, 0), 0.0, 0.2)
        cls.weather_data_7 = WeatherData(4, datetime(2011, 1, 2, 1, 0, 0), 10.0, 0.0)
        cls.barcelona_city_1_weather = [cls.weather_data_6, cls.weather_data_7]

        cls.barcelona_city_2 = City("Barcelona", 5.0, 5.0, id=5)
        cls.weather_data_8 = WeatherData(5, datetime(2010, 2, 2, 0, 0, 0), 5.0, 0.5)
        cls.weather_data_9 = WeatherData(5, datetime(2010, 2, 2, 1, 0, 0), 5.0, 0.0)
        cls.weather_data_10 = WeatherData(5, datetime(2011, 2, 2, 1, 0, 0), 20.0, 1.0)
        cls.barcelona_city_2_weather = [
            cls.weather_data_8,
            cls.weather_data_9,
            cls.weather_data_10,
        ]

    def setUp(self) -> None:
        self.city_repository = Mock(spec=CityRepository)
        self.city_repository.get_all_cities.return_value = [
            self.madrid_city_1,
            self.madrid_city_2,
            self.madrid_city_3,
            self.barcelona_city_1,
            self.barcelona_city_2,
        ]

        self.weather_data_repository = Mock(spec=WeatherDataRepository)

        self.query = GetStatsQuery(
            city_repository=self.city_repository,
            weather_data_repository=self.weather_data_repository,
        )

    def test_execute_for_temperature(self) -> None:
        self.city_repository.get_cities_by_match.return_value = [
            self.madrid_city_1,
            self.madrid_city_2,
            self.madrid_city_3,
        ]
        self.weather_data_repository.get_by_city_id_and_date_range.side_effect = [
            self.madrid_city_1_weather,
            [],
            self.madrid_city_3_weather,
        ]
        stats_query = StatsQuery(
            "Madrid",
            datetime(2001, 1, 1, 0, 0, 0),
            datetime(2020, 1, 1, 0, 0, 0),
            None,
            None,
            20.0,
            -1.0,
        )

        result = self.query.execute_for_temperature(stats_query)

        self.assertEqual(2, len(result.temperature_stats_for_cities))

        self.assertEqual(
            CityTemperatureStats(
                latitude=1.0,
                longitude=1.0,
                temperature_stats=TemperatureStats(
                    average=10.0,
                    average_by_day={"2010-01-01": 10.0},
                    max={"temperature": 12.0, "date_time": "2010-01-01T01:00"},
                    min={"temperature": 8.0, "date_time": "2010-01-01T02:00"},
                    hours_above_threshold=0,
                    hours_below_threshold=0,
                ),
            ).to_dict(),
            result.temperature_stats_for_cities[0].to_dict(),
        )
        self.assertEqual(
            CityTemperatureStats(
                latitude=3.0,
                longitude=3.0,
                temperature_stats=TemperatureStats(
                    average=10.0,
                    average_by_day={"2010-01-06": 10.0},
                    max={"temperature": 15.0, "date_time": "2010-01-06T01:00"},
                    min={"temperature": 5.0, "date_time": "2010-01-06T00:00"},
                    hours_above_threshold=0,
                    hours_below_threshold=0,
                ),
            ).to_dict(),
            result.temperature_stats_for_cities[1].to_dict(),
        )
        self.city_repository.get_cities_by_match.assert_called_once_with(
            "Madrid", None, None
        )
        self.weather_data_repository.get_by_city_id_and_date_range.assert_has_calls(
            [
                call(
                    self.madrid_city_1.id, stats_query.start_date, stats_query.end_date
                ),
                call(
                    self.madrid_city_2.id, stats_query.start_date, stats_query.end_date
                ),
                call(
                    self.madrid_city_3.id, stats_query.start_date, stats_query.end_date
                ),
            ]
        )

    def test_execute_for_precipitation(self) -> None:
        self.city_repository.get_cities_by_match.return_value = [
            self.barcelona_city_1,
            self.barcelona_city_2,
        ]
        self.weather_data_repository.get_by_city_id_and_date_range.side_effect = [
            self.barcelona_city_1_weather,
            self.barcelona_city_2_weather,
        ]
        stats_query = StatsQuery(
            "Barcelona",
            datetime(2001, 1, 1, 0, 0, 0),
            datetime(2020, 1, 1, 0, 0, 0),
            None,
            None,
            30.0,
            0.0,
        )

        result = self.query.execute_for_precipitation(stats_query)

        self.assertEqual(2, len(result.precipitation_stats_for_cities))
        self.assertEqual(
            CityPrecipitationStats(
                latitude=4.0,
                longitude=4.0,
                precipitation_stats=PrecipitationStats(
                    average=0.1,
                    total=0.2,
                    total_by_day={"2011-01-02": 0.2},
                    days_with_precipitation=1,
                    max={"date_time": "2011-01-02T00:00", "precipitation": 0.2},
                ),
            ).to_dict(),
            result.precipitation_stats_for_cities[0].to_dict(),
        )
        self.assertEqual(
            CityPrecipitationStats(
                latitude=5.0,
                longitude=5.0,
                precipitation_stats=PrecipitationStats(
                    average=0.5,
                    total=1.5,
                    total_by_day={"2010-02-02": 0.5, "2011-02-02": 1.0},
                    days_with_precipitation=2,
                    max={"date_time": "2011-02-02T01:00", "precipitation": 1.0},
                ),
            ).to_dict(),
            result.precipitation_stats_for_cities[1].to_dict(),
        )
        self.city_repository.get_cities_by_match.assert_called_once_with(
            "Barcelona", None, None
        )
        self.weather_data_repository.get_by_city_id_and_date_range.assert_has_calls(
            [
                call(
                    self.barcelona_city_1.id,
                    stats_query.start_date,
                    stats_query.end_date,
                ),
                call(
                    self.barcelona_city_2.id,
                    stats_query.start_date,
                    stats_query.end_date,
                ),
            ]
        )

    def test_execute_for_all(self) -> None:
        self.weather_data_repository.get_by_city_id.side_effect = [
            self.madrid_city_1_weather,
            [],
            self.madrid_city_3_weather,
            self.barcelona_city_1_weather,
            self.barcelona_city_2_weather,
        ]

        result = self.query.execute_for_all()

        self.assertEqual(
            2, len(result.weather_stats_by_city.all_city_weather_stats.keys())
        )
        self.assertEqual(
            2, len(result.weather_stats_by_city.all_city_weather_stats["Madrid"])
        )
        self.assertEqual(
            2, len(result.weather_stats_by_city.all_city_weather_stats["Barcelona"])
        )
        self.assertEqual(
            {
                "Barcelona": [
                    {
                        "days_with_precipitation": 1,
                        "end_date": "2011-01-02",
                        "latitude": 4.0,
                        "longitude": 4.0,
                        "precipitation_max": {"date": "2011-01-02T00:00", "value": 0.2},
                        "precipitation_total": 0.2,
                        "start_date": "2011-01-02",
                        "temperature_average": 5.0,
                        "temperature_max": {"date": "2011-01-02T01:00", "value": 10.0},
                        "temperature_min": {"date": "2011-01-02T00:00", "value": 0.0},
                    },
                    {
                        "days_with_precipitation": 2,
                        "end_date": "2011-02-02",
                        "latitude": 5.0,
                        "longitude": 5.0,
                        "precipitation_max": {"date": "2011-02-02T01:00", "value": 1.0},
                        "precipitation_total": 1.5,
                        "start_date": "2010-02-02",
                        "temperature_average": 10.0,
                        "temperature_max": {"date": "2011-02-02T01:00", "value": 20.0},
                        "temperature_min": {"date": "2010-02-02T00:00", "value": 5.0},
                    },
                ],
                "Madrid": [
                    {
                        "days_with_precipitation": 2,
                        "end_date": "2010-01-01",
                        "latitude": 1.0,
                        "longitude": 1.0,
                        "precipitation_max": {"date": "2010-01-01T01:00", "value": 0.2},
                        "precipitation_total": 0.30000000000000004,
                        "start_date": "2010-01-01",
                        "temperature_average": 10.0,
                        "temperature_max": {"date": "2010-01-01T01:00", "value": 12.0},
                        "temperature_min": {"date": "2010-01-01T02:00", "value": 8.0},
                    },
                    {
                        "days_with_precipitation": 1,
                        "end_date": "2010-01-06",
                        "latitude": 3.0,
                        "longitude": 3.0,
                        "precipitation_max": {"date": "2010-01-06T00:00", "value": 0.2},
                        "precipitation_total": 0.2,
                        "start_date": "2010-01-06",
                        "temperature_average": 10.0,
                        "temperature_max": {"date": "2010-01-06T01:00", "value": 15.0},
                        "temperature_min": {"date": "2010-01-06T00:00", "value": 5.0},
                    },
                ],
            },
            result.weather_stats_by_city.to_dict(),
        )
