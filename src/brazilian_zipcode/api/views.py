from dataclasses import asdict
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from .serializers import AddressSerializer
from brazilian_zipcode.service import get_address_info


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def address_info(request: Request):
    zipcode = request.query_params.get("zipcode")
    if not zipcode:
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={"error": "'zipcode' query param required"},
        )

    try:
        address = get_address_info(zipcode)
    except ValidationError:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = AddressSerializer(data=asdict(address))
    serializer.is_valid()
    return Response(data=serializer.data)
