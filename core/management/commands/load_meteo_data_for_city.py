from datetime import datetime

from django.core.management import BaseCommand
from requests import HTTPError

from core.dependency_injection_factories.infrastructure.clients.open_meteo_city_client_factory import (
    OpenMeteoClientFactory,
)
from core.dependency_injection_factories.infrastructure.persistence.repositories.db_city_repository_factory import (
    DbCityRepositoryFactory,
)
from core.dependency_injection_factories.infrastructure.persistence.repositories.db_weather_data_repository_factory import (
    DbWeatherDataRepositoryFactory,
)
from core.domain.clients.meteo_client import MeteoClient
from core.domain.exceptions.city_already_exists_exception import (
    CityAlreadyExistsException,
)
from core.domain.models.city import City
from core.domain.repositories.city_repository import CityRepository
from core.domain.repositories.weather_data_repository import WeatherDataRepository


class Command(BaseCommand):
    help = "Loads temperature and precipitation data within the specified hours from Open-Meteo API for a city."

    def __init__(
        self,
        meteo_client: MeteoClient | None = None,
        city_repository: CityRepository | None = None,
        weather_data_repository: WeatherDataRepository | None = None,
    ):
        super(Command, self).__init__()

        self.__meteo_client = meteo_client or OpenMeteoClientFactory.create()
        self.__city_repository = city_repository or DbCityRepositoryFactory.create()
        self.__weather_data_repository = (
            weather_data_repository or DbWeatherDataRepositoryFactory.create()
        )

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "city_name", type=str, help="The name of the city to load data for."
        )
        parser.add_argument(
            "start_date",
            type=str,
            help="The start date (YYYY-MM-DD).",
        )
        parser.add_argument(
            "end_date",
            type=str,
            help="The end date (YYYY-MM-DD).",
        )
        parser.add_argument(
            "--strategy",
            type=str,
            default="first",
            choices=["first", "all", "select", "index"],
            help='Action to take if multiple cities are found. "first" (default), "all", "select" (interactive), or "index" (requires --index).',
        )
        parser.add_argument(
            "--index",
            type=int,
            help='Index of the city to select when --action is "index".',
        )

    def handle(self, *args, **options) -> None:
        city_name = options["city_name"]

        start_date = options["start_date"]
        start_date_dt = datetime.strptime(start_date, "%Y-%m-%d")

        end_date = options["end_date"]
        end_date_dt = datetime.strptime(end_date, "%Y-%m-%d")

        strategy = options["strategy"]
        index = options.get("index")

        if start_date_dt > end_date_dt:
            raise ValueError(f"{start_date} happens after {end_date}")

        if strategy == "index":
            if index is None:
                raise ValueError("strategy index requires --index")
            elif index < 0:
                raise ValueError("--index is required to be greater or equal to 0!")

        retrieved_cities: list[City]
        try:
            retrieved_cities = self.__meteo_client.get_cities_by_name(city_name)
        except HTTPError as error:
            self.stderr.write(
                f"Error retrieving '{city_name}' from external API. status code: {error.response.status_code}"
            )
            return

        if len(retrieved_cities) == 0:
            self.stdout.write(f"No cities found with the name {city_name}, exiting...")
            return

        if strategy == "index" and index >= len(retrieved_cities):
            self.stderr.write(
                f"There are not enough retrieved cities for the index '{index}'... "
                f"Remember that the index must go from 0 to N-1 being N the number of "
                f"cities retrieved: {len(retrieved_cities)}"
            )
            return

        match strategy:
            case "first":
                self.__process_one_city(retrieved_cities[0], start_date, end_date)
            case "all":
                self.__process_all_cities(retrieved_cities, start_date, end_date)
            case "select":
                self.__process_input(retrieved_cities, start_date, end_date)
            case "index":
                self.__process_one_city(retrieved_cities[index], start_date, end_date)

    def __process_input(
        self, cities: list[City], start_date: str, end_date: str
    ) -> None:
        self.stdout.write("Please, select a city by its number:")
        for i, city in enumerate(cities):
            self.stdout.write(f"{i}. {city}")
        user_input = input(f"Enter number from 0 to {len(cities) - 1}: ")

        try:
            selected_index = int(user_input)
            selected_city = cities[selected_index]
            self.__process_one_city(selected_city, start_date, end_date)
        except (ValueError, IndexError):
            self.stderr.write(
                "Invalid input! It had to be a number within the specified bounds!"
            )

    def __process_one_city(self, city: City, start_date: str, end_date: str) -> None:
        try:
            saved_city = self.__city_repository.save(city)
        except CityAlreadyExistsException as error:
            self.stdout.write(
                f"City '{city.name}' already exists in the database. Skipping insert..."
            )
            city.id = error.city_id
            saved_city = city

        weather_data_list = self.__meteo_client.get_weather_data_by_city(
            saved_city, start_date, end_date
        )

        if len(weather_data_list) == 0:
            self.stdout.write(
                f"No weather data for city '{saved_city.name}' "
                f"[{saved_city.latitude}, {saved_city.longitude}] found in the specified dates!"
            )
            return

        self.__weather_data_repository.bulk_save(weather_data_list)
        self.stdout.write(
            f"City '{saved_city.name}' [{saved_city.latitude}, {saved_city.longitude}] "
            f"weather data successfully inserted from {start_date} to {end_date}!"
        )

    def __process_all_cities(
        self, cities: list[City], start_date: str, end_date: str
    ) -> None:
        [self.__process_one_city(city, start_date, end_date) for city in cities]
