from core.domain.exceptions.validation_error import ValidationError


class FloatFormatValidator:
    @staticmethod
    def validate(name: str, float_str: str | None) -> float | None:
        if float_str is None:
            return None
        try:
            return float(float_str)
        except ValueError:
            raise ValidationError(attr=name, value=float_str)
