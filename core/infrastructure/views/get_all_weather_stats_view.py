from django.http import HttpRequest
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.dependency_injection_factories.application.get_stats.get_stats_query_factory import (
    GetStatsQueryFactory,
)
from core.infrastructure.views.openapi_schemas.all_weather_stats_schema import (
    GetAllWeatherStatsViewSchema,
)
from core.infrastructure.views.openapi_schemas.bad_request_error_schema import (
    BadRequestErrorSchema,
)


class GetAllWeatherStatsView(APIView):
    @swagger_auto_schema(
        tags=["statistics"],
        operation_summary="Obtener estadísticas generales para todas las ciudades en todas las fechas",
        operation_description="Este endpoint obtiene las estadísticas generales las ciudades del sistema para todas"
        " las fechas registradas. Dado que varias ciudades pueden tener el mismo nombre, cada campo ciudad será una"
        " lista con los datos de cada ciudad que se llame igual. Se podrán diferenciar por coordenadas",
        responses={
            200: openapi.Response(
                description="Ok",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={"{{ CITY_NAME }}": GetAllWeatherStatsViewSchema},
                ),
            ),
            400: BadRequestErrorSchema,
        },
    )
    def get(self, _: HttpRequest) -> Response:
        try:
            query = GetStatsQueryFactory.create()
            response = query.execute_for_all()

            return Response(
                response.weather_stats_by_city.to_dict(),
                status.HTTP_200_OK,
            )
        except Exception:
            return Response(
                {"error": "An unexpected error happened"},
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
