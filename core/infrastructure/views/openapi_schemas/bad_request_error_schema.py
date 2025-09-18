from drf_yasg import openapi

BadRequestErrorSchema = openapi.Response(
    description="Bad Request",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "error": openapi.Schema(
                type=openapi.TYPE_STRING,
                example=(
                    "Invalid format for query parameter : {{ QUERY_PARAMETER }} | "
                    "{{ QUERY_PARAMETER }} is required | "
                    "Query parameter {{ QUERY_PARAMETER }} is [lower|greater] than {{ THRESHOLD}}."
                ),
            ),
        },
    ),
)
