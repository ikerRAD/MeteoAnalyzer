from datetime import datetime

from core.domain.exceptions.validation_error import ValidationError


class DateFormatValidator:
    @staticmethod
    def validate(name: str, date_str: str | None) -> datetime | None:
        if date_str is None:
            return None
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            raise ValidationError(attr=name, value=date_str)
