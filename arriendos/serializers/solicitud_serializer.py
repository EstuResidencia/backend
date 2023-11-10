from rest_framework import serializers
from ..models.solicitud import Solicitud


class SolicitudSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solicitud
        fields = [
            "id",
            "usuario",
            "publicacion",
            "estado",
            "pagado",
            "fecha",
            "estado_cambiado",
        ]
