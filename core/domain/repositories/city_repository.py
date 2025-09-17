from abc import ABC, abstractmethod

from core.domain.models.city import City


class CityRepository(ABC):
    @abstractmethod
    def save(self, city: City) -> City:
        pass

    @abstractmethod
    def get_cities_by_match(
        self, name: str, latitude: float | None, longitude: float | None
    ) -> list[City]:
        pass

    @abstractmethod
    def get_all_cities(self) -> list[City]:
        pass
