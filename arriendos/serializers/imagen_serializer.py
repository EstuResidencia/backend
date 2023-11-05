from rest_framework import serializers
from ..models.imagen import Imagen


class ImagenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Imagen
