from abc import ABC, abstractmethod


class Response:
    pass


class Instruction(ABC):
    @abstractmethod
    def handle(self, *args) -> Response:
        pass
