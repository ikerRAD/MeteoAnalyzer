from typing import Any

from core.domain.exceptions.validation_error import ValidationError


class MandatoryValidator:
    @staticmethod
    def validate(name: str, value: Any) -> None:
        if value is None:
            raise ValidationError(message=f"Mandatory field {name} cannot be None")
