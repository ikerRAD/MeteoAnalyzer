from datetime import datetime

from core.domain.models.stats_query import StatsQuery
from core.domain.validators.date_format_validator import DateFormatValidator
from core.domain.validators.float_format_validator import FloatFormatValidator
from core.domain.validators.mandatory_validator import MandatoryValidator
from core.domain.validators.range_validator import RangeValidator


class ValidatorService:
    @staticmethod
    def validate_params(
        city_name: str | None,
        start_date_str: str | None,
        end_date_str: str | None,
        latitude_str: str | None,
        longitude_str: str | None,
        upper_threshold_str: str | None,
        lower_threshold_str: str | None,
    ) -> StatsQuery:
        MandatoryValidator.validate("city_name", city_name)
        MandatoryValidator.validate("start_date", start_date_str)
        MandatoryValidator.validate("end_date", end_date_str)

        start_date = DateFormatValidator.validate("start_date", start_date_str)
        end_date = DateFormatValidator.validate("end_date", end_date_str)

        RangeValidator.validate("start_date", start_date, upper=end_date)

        latitude = FloatFormatValidator.validate("latitude", latitude_str)
        if latitude is not None:
            RangeValidator.validate("latitude", latitude, lower=-90.0, upper=90.0)

        longitude = FloatFormatValidator.validate("longitude", longitude_str)
        if longitude is not None:
            RangeValidator.validate("longitude", longitude, lower=-180.0, upper=180.0)

        return StatsQuery(
            city_name=city_name,
            start_date=start_date,
            end_date=end_date,
            latitude=latitude,
            longitude=longitude,
            upper_threshold=FloatFormatValidator.validate(
                "upper_threshold", upper_threshold_str
            )
            or 30,
            lower_threshold=FloatFormatValidator.validate(
                "lower_threshold", lower_threshold_str
            )
            or 0,
        )
