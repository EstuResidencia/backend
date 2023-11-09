from rest_framework import serializers
from ..models.imagen import Imagen


class ImagenSerializer(serializers.ModelSerializer):
    # Este campo sobre escribe el campo data de la clase Imagen al pasar
    # el objeto por el serializador.
    # Este tipo indica que el valor se lo da un método llamado get_<atributo>
    data = serializers.SerializerMethodField()

    class Meta:
        model = Imagen
        fields = "__all__"

    def get_data(self, imagen: Imagen) -> str:
        return bytes(imagen.data).decode("utf-8")
