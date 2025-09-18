from django.http import HttpRequest
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.dependency_injection_factories.application.get_stats.get_stats_query_factory import (
    GetStatsQueryFactory,
)
from core.domain.models.stats_query import StatsQuery
from core.infrastructure.views.openapi_schemas.bad_request_error_schema import (
    BadRequestErrorSchema,
)
from core.infrastructure.views.openapi_schemas.precipitation_schema import (
    GetPrecipitationViewSchema,
)
from core.infrastructure.views.openapi_schemas.query_parameters import (
    CityNameParam,
    StartDateParam,
    EndDateParam,
    CityLatitudeParam,
    CityLongitudeParam,
)
from core.infrastructure.views.validations.validate_stats_query import (
    validate_stats_query,
)


class GetPrecipitationStatsView(APIView):
    @swagger_auto_schema(
        tags=["statistics"],
        operation_summary="Obtener estadísticas de precipitaciones para ciudad en un rango de fechas",
        operation_description="Este endpoint obtiene las estadísticas de precipitaciones de las ciudades que encajen con la query hecha dado"
        " un rango de fechas. Las ciudades se obtendrán mediante el nombre. Aunque también se puede filtrar por "
        "otros parámetros adicionales",
        responses={
            200: openapi.Response(
                description="Ok",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY, items=GetPrecipitationViewSchema
                ),
            ),
            400: BadRequestErrorSchema,
        },
        manual_parameters=[
            CityNameParam,
            StartDateParam,
            EndDateParam,
            CityLatitudeParam,
            CityLongitudeParam,
        ],
    )
    @validate_stats_query
    def get(self, _: HttpRequest, stats_query: StatsQuery) -> Response:
        query = GetStatsQueryFactory.create()
        response = query.execute_for_precipitation(stats_query)

        return Response(
            [
                city_precipitation_stat.to_dict()
                for city_precipitation_stat in response.precipitation_stats_for_cities
            ],
            status.HTTP_200_OK,
        )
