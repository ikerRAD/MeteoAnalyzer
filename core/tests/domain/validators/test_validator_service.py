from datetime import datetime
from unittest import TestCase

from core.domain.exceptions.validation_error import ValidationError
from core.domain.validators.validator_service import ValidatorService


class TestValidatorService(TestCase):
    def setUp(self) -> None:
        self.valid_start_date = "2023-01-01"
        self.valid_end_date = "2023-01-31"
        self.valid_latitude = "40.7128"
        self.valid_longitude = "-74.0060"
        self.valid_upper = "25.0"
        self.valid_lower = "5.0"

        self.start_date = datetime(2023, 1, 1, 0, 0)
        self.end_date = datetime(2023, 1, 31, 0, 0)
        self.latitude = 40.7128
        self.longitude = -74.0060
        self.upper = 25.0
        self.lower = 5.0

        self.invalid_start_date = "20233-01-01"
        self.invalid_end_date = "2023-1R-31"
        self.invalid_latitude = "40.7.128"
        self.invalid_longitude = "-74.00:60"
        self.invalid_upper = "a25.0"
        self.invalid_lower = "5..0"

    def test_validate(self):
        result = ValidatorService.validate_params(
            "New York",
            self.valid_start_date,
            self.valid_end_date,
            self.valid_latitude,
            self.valid_longitude,
            self.valid_upper,
            self.valid_lower
        )

        self.assertEqual("New York", result.city_name)
        self.assertEqual(self.start_date, result.start_date)
        self.assertEqual(self.end_date, result.end_date)
        self.assertEqual(self.latitude, result.latitude)
        self.assertEqual(self.longitude, result.longitude)
        self.assertEqual(self.upper, result.upper_threshold)
        self.assertEqual(self.lower, result.lower_threshold)

    def test_validate_params_with_optionals_missing(self):
        result = ValidatorService.validate_params(
            "New York",
            self.valid_start_date,
            self.valid_end_date,
            None,
            None,
            None,
            None
        )

        self.assertEqual("New York", result.city_name)
        self.assertEqual(self.start_date, result.start_date)
        self.assertEqual(self.end_date, result.end_date)
        self.assertEqual(None, result.latitude)
        self.assertEqual(None, result.longitude)
        self.assertEqual(30, result.upper_threshold)
        self.assertEqual(0, result.lower_threshold)


    def test_validate_params_without_name(self):
        with self.assertRaisesRegex(ValidationError, "Mandatory field city_name cannot be None"):
            ValidatorService.validate_params(
            None,
            self.valid_start_date,
            self.valid_end_date,
            None,
            None,
            None,
            None
            )


    def test_validate_params_without_start_date(self):
        with self.assertRaisesRegex(ValidationError, "Mandatory field start_date cannot be None"):
            ValidatorService.validate_params(
            "New York",
            None,
            self.valid_end_date,
            None,
            None,
            None,
            None
            )


    def test_validate_params_without_end_date(self):
        with self.assertRaisesRegex(ValidationError, "Mandatory field end_date cannot be None"):
            ValidatorService.validate_params(
            "New York",
            self.valid_start_date,
            None,
            None,
            None,
            None,
            None
            )


    def test_validate_params_with_invalid_start_date(self):
        with self.assertRaisesRegex(ValidationError, f"Invalid format for start_date: {self.invalid_start_date}"):
            ValidatorService.validate_params(
            "New York",
            self.invalid_start_date,
            self.valid_end_date,
            None,
            None,
            None,
            None
            )


    def test_validate_params_with_invalid_end_date(self):
        with self.assertRaisesRegex(ValidationError, f"Invalid format for end_date: {self.invalid_end_date}"):
            ValidatorService.validate_params(
            "New York",
            self.valid_start_date,
            self.invalid_end_date,
            None,
            None,
            None,
            None
            )

    def test_validate_params_with_invalid_latitude(self):
        with self.assertRaisesRegex(ValidationError, f"Invalid format for latitude: {self.invalid_latitude}"):
            ValidatorService.validate_params(
            "New York",
            self.valid_start_date,
            self.valid_end_date,
            self.invalid_latitude,
            None,
            None,
            None
            )

    def test_validate_params_with_invalid_longitude(self):
        with self.assertRaisesRegex(ValidationError, f"Invalid format for longitude: {self.invalid_longitude}"):
            ValidatorService.validate_params(
            "New York",
            self.valid_start_date,
            self.valid_end_date,
            self.valid_latitude,
            self.invalid_longitude,
            None,
            None
            )

    def test_validate_params_with_invalid_upper(self):
        with self.assertRaisesRegex(ValidationError, f"Invalid format for upper_threshold: {self.invalid_upper}"):
            ValidatorService.validate_params(
            "New York",
            self.valid_start_date,
            self.valid_end_date,
            self.valid_latitude,
            self.valid_longitude,
            self.invalid_upper,
            None
            )

    def test_validate_params_with_invalid_lower(self):
        with self.assertRaisesRegex(ValidationError, f"Invalid format for lower_threshold: {self.invalid_lower}"):
            ValidatorService.validate_params(
            "New York",
            self.valid_start_date,
            self.valid_end_date,
            self.valid_latitude,
            self.valid_longitude,
            self.valid_upper,
            self.invalid_lower,
            )


    def test_validate_params_with_start_date_out_of_bounds(self):
        with self.assertRaisesRegex(ValidationError, f"start_date {self.valid_end_date} is greater than {self.valid_start_date}."):
            ValidatorService.validate_params(
            "New York",
            self.valid_end_date,
            self.valid_start_date,
            None,
            None,
            None,
            None
            )

    def test_validate_params_with_latitude_out_of_bounds_upper(self):
        with self.assertRaisesRegex(ValidationError, "latitude 500.0 is greater than 90."):
            ValidatorService.validate_params(
            "New York",
            self.valid_start_date,
            self.valid_end_date,
            "500.0",
            None,
            None,
            None
            )

    def test_validate_params_with_latitude_out_of_bounds_lower(self):
        with self.assertRaisesRegex(ValidationError, "latitude -500.0 is lower than -90."):
            ValidatorService.validate_params(
            "New York",
            self.valid_start_date,
            self.valid_end_date,
            "-500.0",
            None,
            None,
            None
            )

    def test_validate_params_with_longitude_out_of_bounds_upper(self):
        with self.assertRaisesRegex(ValidationError, "longitude 500.0 is greater than 180."):
            ValidatorService.validate_params(
            "New York",
            self.valid_start_date,
            self.valid_end_date,
            self.valid_latitude,
            "500.0",
            None,
            None
            )

    def test_validate_params_with_longitude_out_of_bounds_lower(self):
        with self.assertRaisesRegex(ValidationError, "longitude -500.0 is lower than -180."):
            ValidatorService.validate_params(
            "New York",
            self.valid_start_date,
            self.valid_end_date,
            self.valid_latitude,
            "-500.0",
            None,
            None
            )
