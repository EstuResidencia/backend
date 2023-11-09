from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status

from arriendos.models import Imagen, Publicacion, Solicitud
from arriendos.serializers.imagen_serializer import ImagenSerializer
from arriendos.serializers.publicacion_serializer import PublicacionSerializer
from arriendos.serializers.solicitud_serializer import SolicitudSerializer


@api_view(["GET"])
def notification_signal(request) -> JsonResponse:

    response = {}

    filtered_pubs = Publicacion.objects.filter(estado_cambiado=True)
    pubs_serializer = PublicacionSerializer(data=filtered_pubs, many=True)
    pubs_serializer.is_valid()  # Hay que hacer esto para acceder a al .data.

    response["publicaciones"] = pubs_serializer.data

    filtered_sols = Solicitud.objects.filter(estado_cambiado=True)
    sols_serializer = SolicitudSerializer(data=filtered_sols, many=True)
    sols_serializer.is_valid() # Hay que hacer esto para acceder a al .data.

    response["solicitudes"] = sols_serializer.data

    return JsonResponse(response, status=status.HTTP_200_OK, safe=False)
