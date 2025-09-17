import requests
import pandas as pd
from core.domain.clients.meteo_client import MeteoClient
from core.domain.models.city import City
from core.domain.models.weather_data import WeatherData


class OpenMeteoClient(MeteoClient):
    def __init__(self, city_endpoint_url: str, weather_endpoint_url: str):
        self.__city_endpoint_url = city_endpoint_url
        self.__weather_endpoint_url = weather_endpoint_url

    def get_cities_by_name(self, city_name: str) -> list[City]:
        response = requests.get(self.__city_endpoint_url, params={"name": city_name})

        cities = []
        response.raise_for_status()
        response_json = response.json()
        for city_json in response_json.get("results", []):
            cities.append(
                City(
                    name=city_json["name"],
                    latitude=city_json["latitude"],
                    longitude=city_json["longitude"],
                )
            )

        return cities

    def get_weather_data_by_city(
        self, city: City, start_date: str, end_date: str
    ) -> list[WeatherData]:
        response = requests.get(
            self.__weather_endpoint_url,
            params={
                "latitude": city.latitude,
                "longitude": city.longitude,
                "start_date": start_date,
                "end_date": end_date,
                "hourly": "precipitation,temperature_2m",
            },
        )

        response.raise_for_status()
        response_json = response.json()

        timezone = response_json.get("timezone", "GMT")
        response_dataframe = pd.DataFrame.from_dict(response_json.get("hourly", {}))
        if response_dataframe.empty:
            return []

        response_dataframe["time"] = (
            pd.to_datetime(response_dataframe["time"])
            .dt.tz_localize("UTC")
            .dt.tz_convert(timezone)
        )

        return response_dataframe.apply(
            lambda row: WeatherData(
                date_time=row.time.to_pydatetime(),
                precipitation=row.precipitation,
                temperature=row.temperature_2m,
                city=city,
            ),
            axis=1,
        ).to_list()
