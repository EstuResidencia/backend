from rest_framework.serializers import Serializer
from ..serializers.user_serializer import UserSerializer
from django.contrib.auth import authenticate
from rest_framework import serializers

from ..models.user import User


class UserLoginSerializer(Serializer):
    """
    Serializer class to authenticate users with email and password.
    """

    correo = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user_auth = authenticate(**data)                        #is_active=True
        #user_active = User.objects.filter(correo=data["correo"]).exists()

        if not user_auth:
            raise serializers.ValidationError("Incorrect Credentials")

        return user_auth
