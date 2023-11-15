from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status

from accounts.models import User
from arriendos.models import Publicacion
from arriendos.serializers.publicacion_serializer import PublicacionSerializer


@api_view(["GET", "POST"])
def create_read_publicacion(request) -> JsonResponse:
    if request.method == "GET":
        publicaciones: list = PublicacionSerializer(Publicacion.objects.all(), many=True).data
        return JsonResponse(publicaciones, safe=False, status=status.HTTP_200_OK)

    elif request.method == "POST":
        serializer = PublicacionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data: dict = {"message": "Publicacion fue creada exitosamente", "publicacion": serializer.data}
            return JsonResponse(data, status=status.HTTP_201_CREATED)

        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PATCH", "DELETE", "GET"])
def update_delete_get_publicacion(request, publicacion_id: int) -> JsonResponse:
    try:
        publicacion: Publicacion = Publicacion.objects.get(pk=publicacion_id)

        if request.method == "PATCH":
            if ("inquilino" in request.data) and (request.data["inquilino"]):
                inquilino: User = User.objects.get(pk=request.data["inquilino"])
                publicacion.inquilino = inquilino
                publicacion.save(update_fields=["inquilino"])
                request.data.pop("inquilino")

            for field_name, new_value in request.data.items():
                setattr(publicacion, field_name, new_value)
                publicacion.save(update_fields=[field_name])

            serializer = PublicacionSerializer(publicacion)
            publicacion_data = serializer.data
            publicacion_data.pop("imagenes")
            publicacion_data.pop("calificacion")

            data: dict = {"message": "Publicacion fue actualizada exitosamente", "publicacion": publicacion_data}
            return JsonResponse(data, status=status.HTTP_200_OK)

        elif request.method == "DELETE":
            publicacion.delete()
            return JsonResponse(
                data={"message": "Publicacion fue eliminada exitosamente"},
                status=status.HTTP_200_OK
            )

        elif request.method == "GET":
            serializer = PublicacionSerializer(publicacion)
            return JsonResponse(
                data=serializer.data,
                status=status.HTTP_200_OK
            )

    except Publicacion.DoesNotExist:
        return JsonResponse(
            {"message": "Publicacion no existe"},
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(["GET"])
def read_publicacion_by_arrendador(request, arrendador_id: int) -> JsonResponse:
    try:
        arrendador: User = User.objects.get(pk=arrendador_id)
        publicaciones = PublicacionSerializer(arrendador.publicaciones.all(), many=True)

        return JsonResponse(
            data=publicaciones.data,
            safe=False,
            status=status.HTTP_200_OK
        )

    except User.DoesNotExist:
        return JsonResponse(
            data={"message": "Arrendador no existe"},
            status=status.HTTP_404_NOT_FOUND
        )
