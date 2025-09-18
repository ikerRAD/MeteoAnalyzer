from drf_yasg import openapi

AllWeatherStatsSchema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "start_date": openapi.Schema(
            type=openapi.TYPE_STRING, example="2018-01-10T17:00"
        ),
        "end_date": openapi.Schema(
            type=openapi.TYPE_STRING, example="2020-01-10T17:00"
        ),
        "temperature_average": openapi.Schema(type=openapi.TYPE_NUMBER, example=10.1),
        "precipitation_total": openapi.Schema(type=openapi.TYPE_NUMBER, example=0.1),
        "days_with_precipitation": openapi.Schema(
            type=openapi.TYPE_INTEGER, example=12
        ),
        "precipitation_max": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "value": openapi.Schema(type=openapi.TYPE_NUMBER, example=0.1),
                "date": openapi.Schema(
                    type=openapi.TYPE_STRING, example="2018-01-10T17:00"
                ),
            },
        ),
        "temperature_max": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "value": openapi.Schema(type=openapi.TYPE_NUMBER, example=30.1),
                "date": openapi.Schema(
                    type=openapi.TYPE_STRING, example="2018-01-10T17:00"
                ),
            },
        ),
        "temperature_min": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "value": openapi.Schema(type=openapi.TYPE_NUMBER, example=-0.1),
                "date": openapi.Schema(
                    type=openapi.TYPE_STRING, example="2018-01-10T17:00"
                ),
            },
        ),
    },
)

GetAllWeatherStatsViewSchema = openapi.Schema(
    type=openapi.TYPE_ARRAY,
    items=AllWeatherStatsSchema,
)
