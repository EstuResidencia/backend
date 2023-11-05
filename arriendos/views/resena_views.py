from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status


@api_view(["GET", "POST"])
def create_read_resena(request, publicacion_id: int) -> JsonResponse:
    if request.method == "GET":
        return JsonResponse({"placeholder": "JSON response"}, status=status.HTTP_200_OK)
    elif request.method == "POST":
        return JsonResponse({"placeholder": "JSON response"}, status=status.HTTP_201_CREATED)
