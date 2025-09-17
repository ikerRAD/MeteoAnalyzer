from datetime import datetime, timezone
import unittest
from unittest.mock import Mock, patch, call

from django.core.management.base import OutputWrapper
from requests import HTTPError, Response

from core.domain.exceptions.city_already_exists_exception import (
    CityAlreadyExistsException,
)
from core.domain.models.city import City
from core.domain.models.weather_data import WeatherData
from core.infrastructure.clients.open_meteo_client import OpenMeteoClient
from core.infrastructure.persistence.repositories.db_city_repository import (
    DbCityRepository,
)
from core.infrastructure.persistence.repositories.db_weather_data_repository import (
    DbWeatherDataRepository,
)
from core.management.commands.load_meteo_data_for_city import Command


class TestCommand(unittest.TestCase):
    def setUp(self) -> None:
        self.meteo_client = Mock(spec=OpenMeteoClient)
        self.city_repo = Mock(spec=DbCityRepository)
        self.weather_data_repo = Mock(spec=DbWeatherDataRepository)

        self.command = Command(
            meteo_client=self.meteo_client,
            city_repository=self.city_repo,
            weather_data_repository=self.weather_data_repo,
        )

        self.command.stdout = Mock(spec=OutputWrapper)
        self.command.stderr = Mock(spec=OutputWrapper)

        self.madrid_city_1 = City("Madrid", 40.4165, -3.70256)
        self.madrid_city_2 = City("Madrid", 37.07, -5.19)

        self.madrid_cities = [self.madrid_city_1, self.madrid_city_2]
        self.meteo_client.get_cities_by_name.return_value = self.madrid_cities

        self.barcelona_city = City("Barcelona", 41.3851, 2.1734)

    def test_handle_invalid_date_range(self) -> None:
        with self.assertRaisesRegex(ValueError, "2024-01-02 happens after 2024-01-01"):
            self.command.handle(
                city_name="Madrid",
                start_date="2024-01-02",
                end_date="2024-01-01",
                strategy="first",
            )

    def test_handle_index_strategy_without_index(self) -> None:
        with self.assertRaisesRegex(ValueError, "strategy index requires --index"):
            self.command.handle(
                city_name="Madrid",
                start_date="2024-01-01",
                end_date="2024-01-01",
                strategy="index",
            )

    def test_handle_index_strategy_with_negative_index(self) -> None:
        with self.assertRaisesRegex(
            ValueError, "--index is required to be greater or equal to 0!"
        ):
            self.command.handle(
                city_name="Madrid",
                start_date="2024-01-01",
                end_date="2024-01-01",
                strategy="index",
                index=-1,
            )

    def test_handle_city_not_found(self) -> None:
        self.meteo_client.get_cities_by_name.return_value = []

        self.command.handle(
            city_name="Nonexistent City",
            start_date="2024-01-01",
            end_date="2024-01-01",
            strategy="first",
        )

        self.command.stdout.write.assert_called_once_with(
            "No cities found with the name Nonexistent City, exiting..."
        )
        self.meteo_client.get_cities_by_name.assert_called_once_with("Nonexistent City")

    def test_handle_http_error(self) -> None:
        self.meteo_client.get_cities_by_name.side_effect = HTTPError(
            response=Mock(spec=Response, status_code=500)
        )

        self.command.handle(
            city_name="Barcelona",
            start_date="2024-01-01",
            end_date="2024-01-01",
            strategy="first",
        )

        self.command.stderr.write.assert_called_once_with(
            f"Error retrieving 'Barcelona' from external API. status code: 500"
        )
        self.meteo_client.get_cities_by_name.assert_called_once_with("Barcelona")

    @patch(
        "core.management.commands.load_meteo_data_for_city.Command._Command__process_one_city"
    )
    def test_handle_first_strategy(self, process_one_city: Mock) -> None:
        self.command.handle(
            city_name="Madrid",
            start_date="2024-01-01",
            end_date="2024-01-01",
            strategy="first",
        )

        process_one_city.assert_called_once_with(
            self.madrid_city_1, "2024-01-01", "2024-01-01"
        )
        self.meteo_client.get_cities_by_name.assert_called_once_with("Madrid")

    @patch(
        "core.management.commands.load_meteo_data_for_city.Command._Command__process_all_cities"
    )
    def test_handle_all_strategy(self, process_all_cities: Mock) -> None:
        self.command.handle(
            city_name="Madrid",
            start_date="2024-01-01",
            end_date="2024-01-01",
            strategy="all",
        )

        process_all_cities.assert_called_once_with(
            self.madrid_cities, "2024-01-01", "2024-01-01"
        )
        self.meteo_client.get_cities_by_name.assert_called_once_with("Madrid")

    @patch("builtins.input", side_effect=["1"])
    @patch(
        "core.management.commands.load_meteo_data_for_city.Command._Command__process_one_city"
    )
    def test_handle_select_strategy_with_valid_input(
        self, process_one_city: Mock, *_
    ) -> None:
        self.command.handle(
            city_name="Madrid",
            start_date="2024-01-01",
            end_date="2024-01-01",
            strategy="select",
        )

        process_one_city.assert_called_once_with(
            self.madrid_city_2, "2024-01-01", "2024-01-01"
        )
        self.meteo_client.get_cities_by_name.assert_called_once_with("Madrid")

    @patch("builtins.input", side_effect=["5"])
    def test_handle_select_strategy_with_input_out_of_bounds(self, *_) -> None:
        self.command.handle(
            city_name="Madrid",
            start_date="2024-01-01",
            end_date="2024-01-01",
            strategy="select",
        )

        self.meteo_client.get_cities_by_name.assert_called_once_with("Madrid")
        self.command.stderr.write.assert_called_once_with(
            "Invalid input! It had to be a number within the specified bounds!"
        )

    @patch("builtins.input", side_effect=["a"])
    def test_handle_select_strategy_with_invalid_input(self, *_) -> None:
        self.command.handle(
            city_name="Madrid",
            start_date="2024-01-01",
            end_date="2024-01-01",
            strategy="select",
        )

        self.meteo_client.get_cities_by_name.assert_called_once_with("Madrid")
        self.command.stderr.write.assert_called_once_with(
            "Invalid input! It had to be a number within the specified bounds!"
        )

    @patch(
        "core.management.commands.load_meteo_data_for_city.Command._Command__process_one_city"
    )
    def test_handle_index_strategy(self, process_one_city: Mock) -> None:
        self.command.handle(
            city_name="Madrid",
            start_date="2024-01-01",
            end_date="2024-01-01",
            strategy="index",
            index=1,
        )

        process_one_city.assert_called_once_with(
            self.madrid_city_2, "2024-01-01", "2024-01-01"
        )
        self.meteo_client.get_cities_by_name.assert_called_once_with("Madrid")

    def test_handle_index_strategy_index_out_of_bounds(self) -> None:
        self.meteo_client.get_cities_by_name.return_value = [self.barcelona_city]

        self.command.handle(
            city_name="Barcelona",
            start_date="2024-01-01",
            end_date="2024-01-01",
            strategy="index",
            index=1,
        )

        self.command.stderr.write.assert_called_once_with(
            "There are not enough retrieved cities for the index '1'... "
            "Remember that the index must go from 0 to N-1 being N the number of cities retrieved: 1"
        )
        self.meteo_client.get_cities_by_name.assert_called_once_with("Barcelona")

    def test_process_one_city_success(self) -> None:
        weather_data = [
            WeatherData(
                city_id=self.barcelona_city.id,
                date_time=datetime(2024, 1, 1, hour, tzinfo=timezone.utc),
                temperature=20.0,
                precipitation=hour / 2,
            )
            for hour in range(24)
        ]
        self.meteo_client.get_weather_data_by_city.return_value = weather_data
        self.city_repo.save.return_value = self.barcelona_city

        self.command._Command__process_one_city(
            self.barcelona_city, "2024-01-01", "2024-01-01"
        )

        self.city_repo.save.assert_called_once_with(self.barcelona_city)
        self.weather_data_repo.bulk_save.assert_called_once_with(weather_data)
        self.command.stdout.write.assert_called_with(
            "City 'Barcelona' [41.3851, 2.1734] weather data successfully inserted from 2024-01-01 to 2024-01-01!"
        )

    def test_process_one_city_no_data(self) -> None:
        weather_data = []
        self.meteo_client.get_weather_data_by_city.return_value = weather_data
        self.city_repo.save.return_value = self.barcelona_city

        self.command._Command__process_one_city(
            self.barcelona_city, "2024-01-01", "2024-01-01"
        )

        self.city_repo.save.assert_called_once_with(self.barcelona_city)
        self.weather_data_repo.bulk_save.assert_not_called()
        self.command.stdout.write.assert_called_with(
            "No weather data for city 'Barcelona' [41.3851, 2.1734] found in the specified dates!"
        )

    def test_process_one_city_already_exists(self) -> None:
        weather_data = [
            WeatherData(
                city_id=self.barcelona_city.id,
                date_time=datetime(2024, 1, 1, hour, tzinfo=timezone.utc),
                temperature=20.0,
                precipitation=hour / 2,
            )
            for hour in range(24)
        ]
        self.meteo_client.get_weather_data_by_city.return_value = weather_data
        self.city_repo.save.side_effect = CityAlreadyExistsException(1)

        self.command._Command__process_one_city(
            self.barcelona_city, "2024-01-01", "2024-01-01"
        )

        self.city_repo.save.assert_called_once_with(self.barcelona_city)
        self.weather_data_repo.bulk_save.assert_called_once_with(weather_data)
        self.command.stdout.write.assert_has_calls(
            [
                call(
                    "City 'Barcelona' already exists in the database. Skipping insert..."
                ),
                call(
                    "City 'Barcelona' [41.3851, 2.1734] weather data successfully inserted from 2024-01-01 to 2024-01-01!"
                ),
            ]
        )

        self.barcelona_city.id = None

    @patch(
        "core.management.commands.load_meteo_data_for_city.Command._Command__process_one_city"
    )
    def test_process_all_cities(self, process_one_city) -> None:
        self.command._Command__process_all_cities(
            self.madrid_cities, "2024-01-01", "2024-01-01"
        )

        self.assertEqual(process_one_city.call_count, len(self.madrid_cities))
