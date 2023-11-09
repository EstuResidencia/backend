from rest_framework import serializers

from .imagen_serializer import ImagenSerializer
from ..models.publicacion import Publicacion


class PublicacionSerializer(serializers.ModelSerializer):
    # Estos campos se agregan cuando se meten los datos al serializador.
    # Este tipo indica que el valor se lo da un método llamado get_<atributo>
    calificacion = serializers.SerializerMethodField()
    imagenes = serializers.SerializerMethodField()
    class Meta:
        model = Publicacion
        fields = "__all__"

    def get_calificacion(self, publicacion: Publicacion) -> int:
        resenas = publicacion.resenas.all()

        total = 0
        for resena in resenas:
            total += resena.calificacion

        divisor = len(resenas) if len(resenas) > 0 else 1
        total = round(total / divisor)

        return total

    def get_imagenes(self, publicacion: Publicacion) -> int:
        imagenes = publicacion.imagenes.all()
        imagenes = ImagenSerializer(data=imagenes, many=True)
        imagenes.is_valid()

        return imagenes.data


