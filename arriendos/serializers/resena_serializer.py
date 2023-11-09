from rest_framework import serializers

from accounts.models import User
from ..models import Publicacion
from ..models.resena import Resena


class ResenaSerializer(serializers.ModelSerializer):
    usuario = serializers.SlugRelatedField(
            read_only=True,
            slug_field="nombre"
            )
    class Meta:
        model = Resena
        fields = ("usuario",
                  "comentario",
                  "calificacion",
                  "fecha"
                  )

    def create(self, validated_data):
        validated_data["publicacion"] = Publicacion.objects.get(id=self.initial_data["publicacion"])
        validated_data["usuario"] = User.objects.get(pk=self.initial_data["usuario"])

        return Resena.objects.create(**validated_data)

