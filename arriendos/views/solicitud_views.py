from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status


@api_view(["POST"])
def create_solicitud(request) -> JsonResponse:
    return JsonResponse({"placeholder": "JSON response"}, status=status.HTTP_201_CREATED)


@api_view(["GET", "PATCH", "DELETE"])
def read_update_delete_solicitud(request, solicitud_id: int) -> JsonResponse:
    if request.method == "GET":
        return JsonResponse({"placeholder": "JSON response"}, status=status.HTTP_200_OK)
    elif request.method == "PATCH":
        return JsonResponse({"placeholder": "JSON response"}, status=status.HTTP_200_OK)
    elif request.method == "DELETE":
        return JsonResponse({"placeholder": "JSON response"}, status=status.HTTP_200_OK)


@api_view(["GET"])
def read_solicitud_by_estudiante(request, estudiante_id: int) -> JsonResponse:
    return JsonResponse({"placeholder": "JSON response"}, status=status.HTTP_200_OK)


@api_view(["GET"])
def read_solicitud_by_arrendador(request, arrendador_id: int) -> JsonResponse:
    return JsonResponse({"placeholder": "JSON response"}, status=status.HTTP_200_OK)
