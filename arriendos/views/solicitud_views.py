from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status

from accounts.models import User
from arriendos.models import Solicitud
from arriendos.serializers.solicitud_serializer import SolicitudSerializer


@api_view(["POST"])
def create_solicitud(request) -> JsonResponse:
    serializer = SolicitudSerializer(data=request.data)
    if serializer.is_valid():
        # Check if the user has already made a request for this publication
        solicitud = Solicitud.objects.filter(usuario=request.data["usuario"], publicacion=request.data["publicacion"])

        if solicitud:
            message = {"message": "Ya existe una solicitud para esta publicacion"}
            return JsonResponse(message, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        data = {"message": "Solicitud fue creada exitosamente", "solicitud": serializer.data}

        return JsonResponse(data, status=status.HTTP_201_CREATED)

    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PATCH", "DELETE"])
def read_update_delete_solicitud(request, solicitud_id: int) -> JsonResponse:
    try:
        solicitud: Solicitud = Solicitud.objects.get(pk=solicitud_id)
    except Solicitud.DoesNotExist:
        return JsonResponse({"message": "Solicitud no existe"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = SolicitudSerializer(solicitud)

        return JsonResponse(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "PATCH":
        # save old solicitud data
        old_solicitud = SolicitudSerializer(solicitud).data
        for field_name, new_value in request.data.items():
            setattr(solicitud, field_name, new_value)
            solicitud.save(update_fields=[field_name])

        # Check the object was changed, if so, change estado_cambiado to True
        if old_solicitud != SolicitudSerializer(solicitud).data:
            solicitud.estado_cambiado = True
            solicitud.save(update_fields=["estado_cambiado"])

        serializer = SolicitudSerializer(solicitud)
        solicitud_data = serializer.data
        data = {"message": "Solicitud fue actualizada exitosamente", "solicitud": solicitud_data}

        return JsonResponse(data, status=status.HTTP_200_OK)

    elif request.method == "DELETE":
        solicitud.delete()
        return JsonResponse({"message": "Solicitud fue eliminada exitosamente"}, status=status.HTTP_200_OK)


@api_view(["GET"])
def read_solicitud_by_estudiante(request, estudiante_id: int) -> JsonResponse:
    try:
        estudiante = User.objects.get(pk=estudiante_id)
    except User.DoesNotExist:
        return JsonResponse({"message": "Estudiante no existe"}, status=status.HTTP_404_NOT_FOUND)

    solicitudes = SolicitudSerializer(estudiante.solicitudes.all(), many=True)
    solicitudes_data = solicitudes.data

    return JsonResponse(solicitudes_data, safe=False, status=status.HTTP_200_OK)


@api_view(["GET"])
def read_solicitud_by_arrendador(request, arrendador_id: int) -> JsonResponse:
    try:
        arrendador = User.objects.get(pk=arrendador_id)
    except User.DoesNotExist:
        return JsonResponse({"message": "Arrendador no existe"}, status=status.HTTP_404_NOT_FOUND)

    solicitudes_data = list()

    for publicacion in arrendador.publicaciones.all():
        for solicitud in publicacion.solicitudes.all():
            solicitudes_data.append(SolicitudSerializer(solicitud).data)

    return JsonResponse(solicitudes_data, safe=False, status=status.HTTP_200_OK)
