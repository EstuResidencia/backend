from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from json import loads

from accounts.models import User
from ..models import Publicacion, Solicitud


class CreateReadPublicacionTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.estudiante = User.objects.create(
            nombre="Estudiante",
            correo="estudiante@unal.edu.co",
            celular="310495520",
            password="estudiante",
            rol=2
        )
        self.arrendador = User.objects.create(
            nombre="Arrendador",
            correo="arrendador@unal.edu.co",
            celular="310495520",
            password="arrendador",
            rol=1
        )
        self.publicacion_data = {
            "usuario": self.user.usuario_id,
            "descripcion": "Hogar con ambiente familiar.",
            "direccion": "Calle 30 #35-42",
            "comuna": 11,
            "canon_cop": 800000,
            "area_m2": 30,
            "piso": 1,
            "imagenes": [
                "\xdeadbeef",
                "\xdeaaxvhnj",
                "\xdeasfvghyvl",
            ]
        }
        self.client.login(correo=self.arrendador.correo, password="arrendador")

    def test_create_correct(self):
        response = self.client.post(
            path="/publicacion/",
            data=self.publicacion_data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            Publicacion.objects.last().direccion,
            self.publicacion_data["direccion"]
        )

    def test_create_required_field(self):
        new_publicacion_data = {
            "usuario": self.user.usuario_id,
            "direccion": "Calle 30 #35-42",
            "comuna": 11,
            "canon_cop": 800000,
            "area_m2": 30,
            "piso": 1,
            "imagenes": [
                "\xdeadbeef",
                "\xdeaaxvhnj",
                "\xdeasfvghyvl",
            ]
        }
        response = self.client.post(
            path="/publicacion/",
            data=new_publicacion_data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            loads(response.content),
            {
                "descripcion": [
                    "This field is required."
                ]
            }
        )

    def test_create_unauthenticated(self):
        self.client.logout()
        response = self.client.post(
            path="/publicacion/",
            data=self.publicacion_data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            loads(response.content),
            {
                "detail": "Authentication credentials were not provided."
            }
        )

    def test_create_unauthorized(self):
        self.client.logout()
        self.client.login(correo=self.estudiante.correo, password="estudiante")
        response = self.client.post(
            path="/publicacion/",
            data=self.publicacion_data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            loads(response.content),
            {
                "detail": "You do not have permission to perform this action."
            }
        )

    def test_read_correct(self):
        Publicacion.objects.create(**self.publicacion_data)
        response = self.client.get(path="/publicacion/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # An assertEqual about the response content is missing
        self.assertEqual(
            len(loads(response.content)),
            1
        )


class UpdateDeletePublicacionTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.estudiante = User.objects.create(
            nombre="Estudiante",
            correo="estudiante@unal.edu.co",
            celular="310495520",
            password="estudiante",
            rol=2
        )
        self.arrendador = User.objects.create(
            nombre="Arrendador",
            correo="arrendador@unal.edu.co",
            celular="310495520",
            password="arrendador",
            rol=1
        )
        self.new_publicacion_data = {
            "usuario_id": self.user.usuario_id,
            "inquilino": None,
            "descripcion": "Habitación con ambiente familiar, wifi 500mbs, acceso a zonas comunes y parquedearo.",
            "estado": 1,
            "direccion": "Calle 30 #35-42",
            "comuna": 11,
            "canon_cop": 800000,
            "area_m2": 30,
            "piso": 1,
            "estado_cambiado": False,
        }
        self.publicacion = Publicacion.objects.create(
            usuario=self.arrendador,
            descripcion="Hogar con ambiente familiar.",
            direccion="Calle 30 #35-42",
            comuna=11,
            canon_cop=800000,
            area_m2=30,
            piso=1,
        )
        self.client.login(correo=self.arrendador.correo, password="arrendador")

    def test_update_correct(self):
        response = self.client.patch(
            path=f"/publicacion/{self.publicacion.id}/",
            data=self.new_publicacion_data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Publicacion.objects.get(pk=self.publicacion.id).descripcion,
            self.new_publicacion_data["descripcion"]
        )

    def test_update_unauthenticated(self):
        self.client.logout()
        response = self.client.patch(
            path=f"/publicacion/{self.publicacion.id}/",
            data=self.new_publicacion_data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            loads(response.content),
            {
                "detail": "Authentication credentials were not provided."
            }
        )

    def test_update_unauthorized(self):
        self.client.logout()
        self.client.login(correo=self.estudiante.correo, password="estudiante")
        response = self.client.patch(
            path=f"/publicacion/{self.publicacion.id}/",
            data=self.new_publicacion_data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            loads(response.content),
            {
                "detail": "You do not have permission to perform this action."
            }
        )

    def test_nonexistent_publicacion(self):
        response = self.client.patch(
            path=f"/publicacion/10000/",
            data=self.new_publicacion_data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            loads(response.content),
            {
                "message": "Publicacion no existe"
            }
        )

    def test_delete_correct(self):
        response = self.client.delete(
            path=f"/publicacion/{self.publicacion.id}/",
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Publicacion.objects.filter(pk=self.publicacion.id).count(),
            0
        )


class ReadPublicacionByArrendadorTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.estudiante = User.objects.create(
            nombre="Estudiante",
            correo="estudiante@unal.edu.co",
            celular="310495520",
            password="estudiante",
            rol=2
        )
        self.arrendador = User.objects.create(
            nombre="Arrendador",
            correo="arrendador@unal.edu.co",
            celular="310495520",
            password="arrendador",
            rol=1
        )
        self.publicacion = Publicacion.objects.create(
            usuario=self.arrendador,
            descripcion="Hogar con ambiente familiar.",
            direccion="Calle 30 #35-42",
            comuna=11,
            canon_cop=800000,
            area_m2=30,
            piso=1,
        )
        self.client.login(correo=self.arrendador.correo, password="arrendador")

    def test_read_correct(self):
        response = self.client.get(
            path=f"/publicacion/listar/{self.arrendador.id}/",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(loads(response.content)),
            1
        )

    def test_read_nonexistent(self):
        response = self.client.get(
            path="/publicacion/listar/10000/",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.client(
            loads(response.content),
            {
                "message": "Publicacion no existe"
            }
        )

    def test_read_unauthenticated(self):
        self.client.logout()
        response = self.client.get(
            path=f"/publicacion/listar/{self.arrendador.id}/",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            loads(response.content),
            {
                "detail": "Authentication credentials were not provided."
            }
        )

    def test_read_unauthorized(self):
        self.client.logout()
        self.client.login(correo=self.estudiante.correo, password="estudiante")
        response = self.client.get(
            path=f"/publicacion/listar/{self.arrendador.id}/",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            loads(response.content),
            {
                "detail": "You do not have permission to perform this action."
            }
        )