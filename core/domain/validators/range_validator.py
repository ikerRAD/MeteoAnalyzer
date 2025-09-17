from datetime import datetime

from core.domain.exceptions.validation_error import ValidationError


class RangeValidator:
    @staticmethod
    def validate(
        attr_name: str,
        value: float | datetime,
        upper: float | datetime | None = None,
        lower: float | datetime | None = None,
    ) -> None:
        value_str = (
            str(value) if type(value) is not datetime else value.strftime("%Y-%m-%d")
        )
        if upper is not None and value > upper:
            upper_str = (
                str(upper)
                if type(upper) is not datetime
                else upper.strftime("%Y-%m-%d")
            )
            raise ValidationError(
                f"{attr_name} {value_str} is greater than {upper_str}."
            )

        if lower is not None and value < lower:
            lower_str = (
                str(lower)
                if type(lower) is not datetime
                else lower.strftime("%Y-%m-%d")
            )
            raise ValidationError(f"{attr_name} {value_str} is lower than {lower_str}.")
