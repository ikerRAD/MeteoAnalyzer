from dataclasses import dataclass


@dataclass
class City:
    name: str
    latitude: float
    longitude: float
    id: int | None = None

    def __str__(self):
        return f"{self.name}, [latitude: {self.latitude}, longitude: {self.longitude}]"
