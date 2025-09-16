from core.domain.models.city import City
from core.domain.repositories.city_repository import CityRepository
from core.infrastructure.persistence.models.django_city import DjangoCity


class DbCityRepository(CityRepository):
    def save(self, city: City) -> City:
        django_city = DjangoCity.from_domain(city)
        django_city.save()

        return django_city.to_domain()
