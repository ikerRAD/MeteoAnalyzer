from core.application.get_stats.get_stats_query import GetStatsQuery
from core.dependency_injection_factories.infrastructure.persistence.repositories.db_city_repository_factory import (
    DbCityRepositoryFactory,
)
from core.dependency_injection_factories.infrastructure.persistence.repositories.db_weather_data_repository_factory import (
    DbWeatherDataRepositoryFactory,
)


class GetStatsQueryFactory:
    @staticmethod
    def create() -> GetStatsQuery:
        return GetStatsQuery(
            DbCityRepositoryFactory.create(), DbWeatherDataRepositoryFactory.create()
        )
