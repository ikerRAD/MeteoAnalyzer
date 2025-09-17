class CityAlreadyExistsException(Exception):
    def __init__(self, city_id: int):
        self.city_id = city_id
