from __future__ import annotations
from django.db import models

from core.domain.models.city import City
from core.domain.models.weather_data import WeatherData
from core.infrastructure.persistence.models.django_city import DjangoCity


class DjangoWeatherData(models.Model):
    city = models.ForeignKey(
        DjangoCity, on_delete=models.CASCADE, related_name="weather_data"
    )
    date_time = models.DateTimeField()
    temperature = models.FloatField(null=True, blank=True)
    precipitation = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = "weather_data"
        verbose_name = "weather data"
        verbose_name_plural = "weather data"
        ordering = ["date_time"]
        unique_together = ("city", "date_time")
        indexes = [
            models.Index(fields=["city", "date_time"]),
        ]

    def __str__(self):
        return f"{self.city.name} - {self.date_time.strftime('%Y-%m-%d %H:%M')}"

    @staticmethod
    def from_domain(weather_data: WeatherData) -> DjangoWeatherData:
        return DjangoWeatherData(
            city_id=weather_data.city.id,
            date_time=weather_data.date_time,
            temperature=weather_data.temperature,
            precipitation=weather_data.precipitation,
        )

    def to_domain(self) -> WeatherData:
        city_domain_instance = City(
            id=self.city.id,
            name=self.city.name,
            latitude=self.city.latitude,
            longitude=self.city.longitude,
        )

        return WeatherData(
            id=self.id,
            city=city_domain_instance,
            date_time=self.date_time,
            temperature=self.temperature,
            precipitation=self.precipitation,
        )
