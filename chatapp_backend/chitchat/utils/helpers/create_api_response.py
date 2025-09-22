from rest_framework import status
from rest_framework.response import Response


def create_api_response(
    success=True,
    message="",
    data=None,
    errors=None,
    http_status=status.HTTP_200_OK,
    **kwargs
):
    response = {
        "success": success,
        "message": message,
    }
    if data is not None:
        response["data"] = data
    if errors is not None:
        response["errors"] = errors

    response.update(kwargs)
    return Response(response, status=http_status)
