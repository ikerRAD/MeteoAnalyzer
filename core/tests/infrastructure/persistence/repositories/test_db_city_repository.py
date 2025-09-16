from django.test import TestCase

from core.domain.models.city import City
from core.infrastructure.persistence.models.django_city import DjangoCity
from core.infrastructure.persistence.repositories.db_city_repository import (
    DbCityRepository,
)


class TestIntegrationDbCityRepository(TestCase):
    def setUp(self) -> None:
        self.db_city_repository = DbCityRepository()

    def test_save(self) -> None:
        cities: list[DjangoCity] = list(DjangoCity.objects.all())
        self.assertEqual([], cities)

        domain_city = self.db_city_repository.save(City("Nowhere", 0.0, 0.0))

        cities = list(DjangoCity.objects.all())
        self.assertEqual(1, len(cities))

        city = cities[0]
        self.assertEqual("Nowhere", city.name)
        self.assertEqual(0.0, city.longitude)
        self.assertEqual(0.0, city.latitude)
        self.assertEqual(domain_city, city.to_domain())

        city.delete()
