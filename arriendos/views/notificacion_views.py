from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status


@api_view(["GET"])
def notification_signal(request) -> JsonResponse:
    return JsonResponse({"placeholder": "JSON response"}, status=status.HTTP_200_OK)
