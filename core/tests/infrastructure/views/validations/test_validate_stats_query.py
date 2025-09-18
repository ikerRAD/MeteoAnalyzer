from datetime import datetime
from unittest import TestCase
from unittest.mock import patch

from django.test import RequestFactory
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.domain.exceptions.validation_error import ValidationError
from core.domain.models.stats_query import StatsQuery
from core.domain.validators.validator_service import ValidatorService
from core.infrastructure.views.validations.validate_stats_query import (
    validate_stats_query,
)


class DummyView(APIView):
    @validate_stats_query
    def get(self, _, stats_query: StatsQuery):
        return Response(
            {"message": "Success", "query": stats_query.__dict__}, status=200
        )


class TestValidateStatsQueryDecorator(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.view = DummyView.as_view()

    @patch.object(ValidatorService, "validate_params")
    def test_valid_params(self, mock_validate):
        mock_validate.return_value = StatsQuery(
            "Madrid",
            datetime(2001, 1, 1, 0, 0, 0),
            datetime(2002, 1, 1, 0, 0, 0),
            None,
            None,
            31.0,
            3.0,
        )

        request = self.factory.get("/dummy-url/?city=Madrid")
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["query"]["city_name"], "Madrid")

    @patch.object(ValidatorService, "validate_params")
    def test_validation_error(self, mock_validate):
        mock_validate.side_effect = ValidationError("Invalid date format")

        request = self.factory.get("/dummy-url/?start_date=invalid")
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Invalid date format")

    @patch.object(ValidatorService, "validate_params")
    def test_internal_server_error(self, mock_validate):
        mock_validate.side_effect = ValueError("Some unexpected error")

        request = self.factory.get("/dummy-url/")
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data["error"], "An unexpected error happened")
        self.assertNotIn("message", response.data)
