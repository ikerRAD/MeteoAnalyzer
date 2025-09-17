from MeteoAnalyzer.settings import OPEN_METEO_CITY_ENDPOINT, OPEN_METEO_WEATHER_ENDPOINT
from core.infrastructure.clients.open_meteo_client import OpenMeteoClient


class OpenMeteoClientFactory:
    @staticmethod
    def create() -> OpenMeteoClient:
        return OpenMeteoClient(OPEN_METEO_CITY_ENDPOINT, OPEN_METEO_WEATHER_ENDPOINT)
