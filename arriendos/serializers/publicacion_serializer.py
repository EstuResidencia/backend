from rest_framework import serializers

from .imagen_serializer import ImagenSerializer
from ..models import Imagen, Resena
from ..models.publicacion import Publicacion


class PublicacionSerializer(serializers.ModelSerializer):
    # Estos campos se agregan cuando se meten los datos al serializador.
    # Este tipo indica que el valor se lo da un método llamado get_<atributo>
    calificacion = serializers.SerializerMethodField()
    imagenes = serializers.SerializerMethodField()
    class Meta:
        model = Publicacion
        fields = [
            "id",
            "usuario",
            "inquilino",
            "descripcion",
            "estado",
            "direccion",
            "comuna",
            "canon_cop",
            "area_m2",
            "piso",
            "comuna",
            "estado_cambiado",
            "calificacion",
            "imagenes"
        ]

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


    def create(self, validated_data):
        imagenes: list = self.initial_data.pop("imagenes")
        publicacion = Publicacion.objects.create(**validated_data)
        for imagen in imagenes:
            Imagen.objects.create(publicacion=publicacion, data=bytes(imagen, "utf-8"))

        return publicacion