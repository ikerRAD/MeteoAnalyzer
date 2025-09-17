from drf_yasg import openapi

CityNameParam = openapi.Parameter(
    "city",
    openapi.IN_QUERY,
    description="Nombre de la ciudad.",
    type=openapi.TYPE_STRING,
    required=True,
)

CityLatitudeParam = openapi.Parameter(
    "latitude",
    openapi.IN_QUERY,
    description="Latitud de la ciudad. Rango [-90,90]",
    type=openapi.TYPE_NUMBER,
    required=False,
)

CityLongitudeParam = openapi.Parameter(
    "longitude",
    openapi.IN_QUERY,
    description="Longitud de la ciudad. Rango [-180,180]",
    type=openapi.TYPE_NUMBER,
    required=False,
)

StartDateParam = openapi.Parameter(
    "start_date",
    openapi.IN_QUERY,
    description="Fecha de inicio del rango en formato YYYY-MM-DD.",
    type=openapi.TYPE_STRING,
    required=True,
)

EndDateParam = openapi.Parameter(
    "end_date",
    openapi.IN_QUERY,
    description="Fecha de fin del rango en formato YYYY-MM-DD.",
    type=openapi.TYPE_STRING,
    required=True,
)

UpperThresholdParam = openapi.Parameter(
    "upper_threshold",
    openapi.IN_QUERY,
    description="Umbral superior.",
    type=openapi.TYPE_NUMBER,
    required=False,
)

LowerThresholdParam = openapi.Parameter(
    "lower_threshold",
    openapi.IN_QUERY,
    description="Umbral inferior.",
    type=openapi.TYPE_NUMBER,
    required=False,
)
