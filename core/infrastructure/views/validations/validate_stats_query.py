from functools import wraps
from typing import Callable

from django.http import HttpRequest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.domain.exceptions.validation_error import ValidationError
from core.domain.validators.validator_service import ValidatorService


def validate_stats_query(
    func: Callable[[APIView, HttpRequest, ...], Response]
) -> Callable[[APIView, HttpRequest, dict, ...], Response] | Response:
    @wraps(func)
    def wrapper(
        self, request: HttpRequest, *args, **kwargs
    ) -> Callable[[APIView, HttpRequest, dict, ...], Response] | Response:
        try:
            kwargs["stats_query"] = ValidatorService.validate_params(
                city_name=request.GET.get("city"),
                start_date_str=request.GET.get("start_date"),
                end_date_str=request.GET.get("end_date"),
                latitude_str=request.GET.get("latitude"),
                longitude_str=request.GET.get("longitude"),
                upper_threshold_str=request.GET.get("upper_threshold"),
                lower_threshold_str=request.GET.get("lower_threshold"),
            )

            return func(self, request, *args, **kwargs)
        except ValidationError as error:
            return Response({"error": str(error)}, status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response(
                {"error": "An unexpected error happened"},
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    return wrapper
