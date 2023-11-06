from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from ..models.solicitud import Solicitud
from ..models.publicacion import Publicacion
from accounts.models.user import User


class CreateSolicitudTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            nombre="Calypso",
            correo="calypso@unal.edu.co",
            celular="310495520",
            password="calypso"
        )
        self.arrendador = User.objects.create(
            nombre="Carlitos",
            correo="carlitos@gmail.com",
            celular="3104153021",
            password="carlitos"
        )
        self.client.force_authenticate(self.user)
        self.publicacion = Publicacion.objects.create(
            usuario=self.arrendador,
            descripcion="Publicacion de prueba",
            direccion="Calle 123",
            canon_cop=1000000,
            area_m2=100,
            piso=1,
            comuna=1
        )

    def test_create_solicitud_correct(self):
        # Datos de ejemplo para la solicitud
        solicitud_data = {
            "usuario": self.user.id,
            "publicacion": self.publicacion.id,
        }

        # Realiza una solicitud POST para crear una solicitud
        response = self.client.post("/solicitud/", solicitud_data, format='json')

        self.assertEqual(response.status_code, 201)  # 201 Creado
        solicitud = Solicitud.objects.get(id=response.data['solicitud']['id'])
        self.assertEqual(solicitud.estado, 1)  # Verifica que el estado sea PENDIENTE
        self.assertEqual(solicitud.pagado, False)  # Verifica que pagado sea False

    def test_create_solicitud_invalid_data(self):
        # Datos de solicitud con campos faltantes
        solicitud_data = {}

        # Realiza una solicitud POST con datos incompletos
        response = self.client.post("/solicitud/", solicitud_data, format='json')

        self.assertEqual(response.status_code, 400)  # 400 Bad Request

    def test_create_solicitud_not_found(self):
        # Intenta crear una solicitud para una publicación inexistente (publicacion_id)
        solicitud_data = {
            "usuario": self.user.id,
            "publicacion": 999,  # ID inexistente
        }

        response = self.client.post("/solicitud/", solicitud_data, format='json')

        self.assertEqual(response.status_code, 400)  # 400 Bad Request

    def test_create_solicitud_existing_solicitud(self):
        # Intenta crear una solicitud duplicada
        solicitud_data = {
            "usuario": self.user.id,
            "publicacion": self.publicacion.id,
        }

        # Crea una solicitud inicialmente
        response1 = self.client.post("/solicitud/", solicitud_data, format='json')

        self.assertEqual(response1.status_code, 201)  # 201 Creado

        # Intenta crear la misma solicitud nuevamente
        response2 = self.client.post("/solicitud/", solicitud_data, format='json')

        self.assertEqual(response2.status_code, 400)  # 400 Bad Request
