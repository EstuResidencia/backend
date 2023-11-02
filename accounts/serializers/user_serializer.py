from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from ..models.user import User


class UserSerializer(ModelSerializer):
    # write_only means that the field will not be returned in the response
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("usuario_id",
                  "nombre",
                  "correo",
                  "tipo_documento",
                  "documento",
                  "password",
                  "celular",
                  "validado",
                  "rol")

    def create(self, validated_data):
        usuario = User.objects.create_user(**validated_data)

        return usuario