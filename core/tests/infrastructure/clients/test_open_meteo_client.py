from unittest import TestCase
from unittest.mock import patch, Mock
import pandas as pd
from requests import Response, HTTPError

from core.domain.models.city import City
from core.domain.models.weather_data import WeatherData
from core.infrastructure.clients.open_meteo_client import OpenMeteoClient


class TestOpenMeteoClient(TestCase):
    def setUp(self) -> None:
        self.city_endpoint = "http://fake-city-api.com/v1/search"
        self.weather_endpoint = "http://fake-weather-api.com/v1/archive"

        self.client = OpenMeteoClient(self.city_endpoint, self.weather_endpoint)

    @patch("requests.get")
    def test_get_cities_by_name(self, get: Mock):
        response = Mock(spec=Response)
        response.status_code = 200
        response.json.return_value = {
            "results": [
                {"name": "Madrid", "latitude": 40.4165, "longitude": -3.70256},
                {"name": "Madrid", "latitude": 37.07, "longitude": -5.19},
            ]
        }
        get.return_value = response

        cities = self.client.get_cities_by_name("Madrid")

        get.assert_called_once_with(self.city_endpoint, params={"name": "Madrid"})

        self.assertEqual(len(cities), 2)
        self.assertEqual(City("Madrid", 40.4165, -3.70256), cities[0])
        self.assertEqual(City("Madrid", 37.07, -5.19), cities[1])

    @patch("requests.get")
    def test_get_cities_by_name_not_found(self, get: Mock) -> None:
        response = Mock(spec=Response)
        response.status_code = 200
        response.json.return_value = {"results": []}
        get.return_value = response

        cities = self.client.get_cities_by_name("NonExistentCity")

        self.assertEqual([], cities)

    @patch("requests.get")
    def test_get_cities_by_name_http_error(self, get: Mock) -> None:
        response = Mock(spec=Response)
        response.status_code = 404
        response.raise_for_status.side_effect = HTTPError
        get.return_value = response

        with self.assertRaises(HTTPError):
            self.client.get_cities_by_name("AnyCity")

    @patch("requests.get")
    def test_get_weather_data_by_city_success(self, get: Mock) -> None:
        response = Mock(spec=Response)
        response.status_code = 200
        response.json.return_value = {
            "hourly": {
                "time": ["2025-01-01T00:00", "2025-01-01T01:00"],
                "precipitation": [0.1, 0.2],
                "temperature_2m": [15.5, 16.0],
            },
            "timezone": "Europe/Madrid",
        }
        get.return_value = response

        test_city = City("Madrid", 40.4165, -3.70256)
        weather_data = self.client.get_weather_data_by_city(
            test_city, "2025-01-01", "2025-01-01"
        )

        get.assert_called_once_with(
            self.weather_endpoint,
            params={
                "latitude": 40.4165,
                "longitude": -3.70256,
                "start_date": "2025-01-01",
                "end_date": "2025-01-01",
                "hourly": "precipitation,temperature_2m",
            },
        )

        self.assertEqual(len(weather_data), 2)
        self.assertEqual(
            WeatherData(
                test_city,
                date_time=pd.to_datetime("2025-01-01T00:00").tz_localize("UTC").tz_convert("Europe/Madrid").to_pydatetime(),
                precipitation=0.1,
                temperature=15.5,
            ),
            weather_data[0],
        )
        self.assertEqual(
            WeatherData(
                test_city,
                date_time=pd.to_datetime("2025-01-01T01:00").tz_localize("UTC").tz_convert("Europe/Madrid").to_pydatetime(),
                precipitation=0.2,
                temperature=16.0,
            ),
            weather_data[1],
        )

    @patch("requests.get")
    def test_get_weather_data_empty(self, get: Mock) -> None:
        response = Mock(spec=Response)
        response.status_code = 200
        response.json.return_value = {"hourly": {}, "timezone": "Europe/Madrid"}
        get.return_value = response

        test_city = City("Madrid", 40.4165, -3.70256)
        weather_data = self.client.get_weather_data_by_city(
            test_city, "2025-01-01", "2025-01-01"
        )

        self.assertEqual(weather_data, [])
