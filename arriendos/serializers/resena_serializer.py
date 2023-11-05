from rest_framework import serializers
from ..models.resena import Resena


class ResenaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resena
