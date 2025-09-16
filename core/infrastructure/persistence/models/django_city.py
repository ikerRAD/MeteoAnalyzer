from __future__ import annotations
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from core.domain.models.city import City


class DjangoCity(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField(
        validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)]
    )
    longitude = models.FloatField(
        validators=[MinValueValidator(-180.0), MaxValueValidator(180.0)]
    )

    class Meta:
        db_table = "cities"
        verbose_name = "city"
        verbose_name_plural = "cities"

    def __str__(self):
        return f"{self.name}, [latitude: {self.latitude}, longitude: {self.longitude}]"

    @staticmethod
    def from_domain(city: City) -> DjangoCity:
        return DjangoCity(
            name=city.name,
            latitude=city.latitude,
            longitude=city.longitude,
        )

    def to_domain(self) -> City:
        return City(
            id=self.id, name=self.name, latitude=self.latitude, longitude=self.longitude
        )
