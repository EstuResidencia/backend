from rest_framework import serializers
from ..models.publicacion import Publicacion


class PublicacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publicacion
