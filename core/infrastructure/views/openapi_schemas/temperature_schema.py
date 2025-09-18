from drf_yasg import openapi

TemperatureSchema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "average": openapi.Schema(type=openapi.TYPE_NUMBER, example=23.1),
        "average_by_day": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "YYYY-MM-DD": openapi.Schema(type=openapi.TYPE_NUMBER, example=23.1)
            },
        ),
        "max": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "value": openapi.Schema(type=openapi.TYPE_NUMBER, example=33.1),
                "date": openapi.Schema(
                    type=openapi.TYPE_STRING, example="2018-01-10T17:00"
                ),
            },
        ),
        "min": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "value": openapi.Schema(type=openapi.TYPE_NUMBER, example=13.1),
                "date": openapi.Schema(
                    type=openapi.TYPE_STRING, example="2018-01-10T22:00"
                ),
            },
        ),
        "hours_above_threshold": openapi.Schema(type=openapi.TYPE_INTEGER, example=5),
        "hours_below_threshold": openapi.Schema(type=openapi.TYPE_INTEGER, example=2),
    },
)

GetTemperatureViewSchema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "latitude": openapi.Schema(type=openapi.TYPE_NUMBER, example=-3.12),
        "longitude": openapi.Schema(type=openapi.TYPE_NUMBER, example=-70.23),
        "temperature": TemperatureSchema,
    },
)
