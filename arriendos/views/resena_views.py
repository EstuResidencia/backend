from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status

from arriendos.models import Publicacion
from arriendos.serializers.resena_serializer import ResenaSerializer


@api_view(["GET", "POST"])
def create_read_resena(request, publicacion_id: int) -> JsonResponse:
    if request.method == "GET":
        try:
            publicacion = Publicacion.objects.get(id=publicacion_id)
            serializer = ResenaSerializer(publicacion.resenas.all(), many=True)

            return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)

        except Publicacion.DoesNotExist:
            return JsonResponse({"message": "La publicación no existe"}, status=status.HTTP_404_NOT_FOUND)

    elif request.method == "POST":
        data = request.data.copy()

        data["publicacion"] = publicacion_id
        serializer = ResenaSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            response = {"message": "Resena fue creada exitosamente",
                        "resena": serializer.data
                        }
            return JsonResponse(response, status=status.HTTP_201_CREATED)
        response = serializer.errors
        response["message"] = "Hubo un error al crear la reseña."
        return JsonResponse(response, status=status.HTTP_400_BAD_REQUEST)
