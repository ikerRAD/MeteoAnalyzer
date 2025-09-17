from core.infrastructure.persistence.repositories.db_weather_data_repository import (
    DbWeatherDataRepository,
)


class DbWeatherDataRepositoryFactory:
    @staticmethod
    def create() -> DbWeatherDataRepository:
        return DbWeatherDataRepository()
