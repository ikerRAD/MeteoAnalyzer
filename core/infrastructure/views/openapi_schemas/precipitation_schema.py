from drf_yasg import openapi

PrecipitationSchema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "total": openapi.Schema(type=openapi.TYPE_NUMBER, example=0.1),
        "total_by_day": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "YYYY-MM-DD": openapi.Schema(type=openapi.TYPE_NUMBER, example=0.1)
            },
        ),
        "days_with_precipitation": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
        "max": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "value": openapi.Schema(type=openapi.TYPE_NUMBER, example=0.1),
                "date": openapi.Schema(
                    type=openapi.TYPE_STRING, example="2018-01-10T17:00"
                ),
            },
        ),
        "average": openapi.Schema(type=openapi.TYPE_NUMBER, example=0.1),
    },
)

GetPrecipitationViewSchema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "latitude": openapi.Schema(type=openapi.TYPE_NUMBER, example=-3.12),
        "longitude": openapi.Schema(type=openapi.TYPE_NUMBER, example=-70.23),
        "precipitation": PrecipitationSchema,
    },
)
