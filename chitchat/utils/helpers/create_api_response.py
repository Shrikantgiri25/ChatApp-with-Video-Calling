from rest_framework import status
from rest_framework.response import Response


def create_api_response(
    message, data=None, errors=None, http_status=status.HTTP_200_OK, **kwargs
):

    response = {"message": message}
    if data:
        response["data"] = data
    if errors:
        response["errors"] = errors

    response.update(kwargs)
    return Response(response, status=http_status)
