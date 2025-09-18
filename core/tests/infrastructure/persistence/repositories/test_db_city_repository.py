from django.test import TestCase

from core.domain.exceptions.city_already_exists_exception import (
    CityAlreadyExistsException,
)
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

    def test_save_already_existing(self) -> None:
        cities: list[DjangoCity] = list(DjangoCity.objects.all())
        self.assertEqual([], cities)

        DjangoCity.objects.create(name="Nowhere", longitude=0.0, latitude=0.0)

        cities: list[DjangoCity] = list(DjangoCity.objects.all())

        self.assertEqual(1, len(cities))
        self.assertEqual("Nowhere", cities[0].name)
        self.assertEqual(0.0, cities[0].longitude)
        self.assertEqual(0.0, cities[0].latitude)

        with self.assertRaises(CityAlreadyExistsException) as context:
            self.db_city_repository.save(City("Nowhere", 0.0, 0.0))

            self.assertEqual(cities[0].id, context.exception.city_id)

            cities[0].delete()

    def test_get_cities_by_match(self) -> None:
        city_1 = DjangoCity.objects.create(
            id=1, name="Nowhere", longitude=0.0, latitude=2.0
        )
        city_2 = DjangoCity.objects.create(
            id=2, name="Nowhere", longitude=1.0, latitude=1.0
        )
        city_3 = DjangoCity.objects.create(
            id=3, name="Nowhere", longitude=1.0, latitude=2.0
        )

        cities = self.db_city_repository.get_cities_by_match("Nowhere", None, None)

        self.assertEqual(3, len(cities))
        self.assertCountEqual(
            [city_1.to_domain(), city_2.to_domain(), city_3.to_domain()], cities
        )

        city_1.delete()
        city_2.delete()
        city_3.delete()

    def test_get_cities_by_match_with_latitude(self) -> None:
        city_1 = DjangoCity.objects.create(
            id=1, name="Nowhere", longitude=0.0, latitude=2.0
        )
        city_2 = DjangoCity.objects.create(
            id=2, name="Nowhere", longitude=1.0, latitude=1.0
        )
        city_3 = DjangoCity.objects.create(
            id=3, name="Nowhere", longitude=1.0, latitude=2.0
        )

        cities = self.db_city_repository.get_cities_by_match("Nowhere", 2.0, None)

        self.assertEqual(2, len(cities))
        self.assertCountEqual([city_1.to_domain(), city_3.to_domain()], cities)

        city_1.delete()
        city_2.delete()
        city_3.delete()

    def test_get_cities_by_match_with_longitude(self) -> None:
        city_1 = DjangoCity.objects.create(
            id=1, name="Nowhere", longitude=0.0, latitude=2.0
        )
        city_2 = DjangoCity.objects.create(
            id=2, name="Nowhere", longitude=1.0, latitude=1.0
        )
        city_3 = DjangoCity.objects.create(
            id=3, name="Nowhere", longitude=1.0, latitude=2.0
        )

        cities = self.db_city_repository.get_cities_by_match("Nowhere", None, 1.0)

        self.assertEqual(2, len(cities))
        self.assertCountEqual([city_2.to_domain(), city_3.to_domain()], cities)

        city_1.delete()
        city_2.delete()
        city_3.delete()

    def test_get_cities_by_match_with_latitude_and_longitude(self) -> None:
        city_1 = DjangoCity.objects.create(
            id=1, name="Nowhere", longitude=0.0, latitude=2.0
        )
        city_2 = DjangoCity.objects.create(
            id=2, name="Nowhere", longitude=1.0, latitude=1.0
        )
        city_3 = DjangoCity.objects.create(
            id=3, name="Nowhere", longitude=1.0, latitude=2.0
        )

        cities = self.db_city_repository.get_cities_by_match("Nowhere", 1.0, 1.0)

        self.assertEqual(1, len(cities))
        self.assertCountEqual([city_2.to_domain()], cities)

        city_1.delete()
        city_2.delete()
        city_3.delete()

    def test_get_all_cities(self) -> None:
        city_1 = DjangoCity.objects.create(
            id=1, name="Nowhere", longitude=0.0, latitude=2.0
        )
        city_2 = DjangoCity.objects.create(
            id=2, name="Nowhere", longitude=1.0, latitude=1.0
        )
        city_3 = DjangoCity.objects.create(
            id=3, name="Nowhere", longitude=1.0, latitude=2.0
        )
        city_4 = DjangoCity.objects.create(
            id=4, name="Elsewhere", longitude=3.0, latitude=2.0
        )
        city_5 = DjangoCity.objects.create(
            id=5, name="Somewhere", longitude=4.0, latitude=2.0
        )

        cities = self.db_city_repository.get_all_cities()

        self.assertEqual(5, len(cities))
        self.assertCountEqual(
            [
                city_1.to_domain(),
                city_2.to_domain(),
                city_3.to_domain(),
                city_4.to_domain(),
                city_5.to_domain(),
            ],
            cities,
        )

        city_1.delete()
        city_2.delete()
        city_3.delete()
        city_4.delete()
        city_5.delete()
