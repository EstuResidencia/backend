from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status


@api_view(["GET", "POST"])
def create_read_publicacion(request) -> JsonResponse:
    if request.method == "GET":
        return JsonResponse({"placeholder": "JSON response"}, status=status.HTTP_200_OK)
    elif request.method == "POST":
        return JsonResponse({"placeholder": "JSON response"}, status=status.HTTP_201_CREATED)

@api_view(["PATCH", "DELETE"])
def update_delete_publicacion(request, publicacion_id: int) -> JsonResponse:
    if request.method == "PATCH":
        return JsonResponse({"placeholder": "JSON response"}, status=status.HTTP_200_OK)
    elif request.method == "DELETE":
        return JsonResponse({"placeholder": "JSON response"}, status=status.HTTP_200_OK)

@api_view(["GET"])
def read_publicacion_by_arrendador(request, arrendador_id: int) -> JsonResponse:
    return JsonResponse({"placeholder": "JSON response"}, status=status.HTTP_200_OK)
