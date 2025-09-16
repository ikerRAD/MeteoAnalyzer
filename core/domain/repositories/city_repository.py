from abc import ABC, abstractmethod

from core.domain.models.city import City


class CityRepository(ABC):
    @abstractmethod
    def save(self, city: City) -> City:
        pass
