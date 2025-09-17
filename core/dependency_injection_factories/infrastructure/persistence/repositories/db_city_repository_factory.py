from core.infrastructure.persistence.repositories.db_city_repository import (
    DbCityRepository,
)


class DbCityRepositoryFactory:
    @staticmethod
    def create() -> DbCityRepository:
        return DbCityRepository()
