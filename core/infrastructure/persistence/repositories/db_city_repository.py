from django.db import IntegrityError, transaction

from core.domain.exceptions.city_already_exists_exception import (
    CityAlreadyExistsException,
)
from core.domain.models.city import City
from core.domain.repositories.city_repository import CityRepository
from core.infrastructure.persistence.models.django_city import DjangoCity


class DbCityRepository(CityRepository):
    def __init__(self):
        self.__django_city_manager = DjangoCity.objects

    def save(self, city: City) -> City:
        try:
            with transaction.atomic():
                django_city = DjangoCity.from_domain(city)
                django_city.save()
                return django_city.to_domain()
        except IntegrityError:
            saved_django_city = self.__django_city_manager.get(latitude=city.latitude, longitude=city.longitude, name=city.name)
            raise CityAlreadyExistsException(saved_django_city.id)
