from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from json import loads
from datetime import datetime

from accounts.models import User
from ..models import Publicacion, Imagen


class CreateReadPublicacionTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.arrendador = User.objects.create(
            nombre="Arrendador",
            correo="arrendador@unal.edu.co",
            celular="310495520",
            password="arrendador",
            rol=1
        )
        self.publicacion_data: dict = {
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
            ]
        }
        self.correct_response: dict = {
            "message": "Publicacion fue creada exitosamente",
            "publicacion": {
                "id": 1,
                "usuario": self.arrendador.usuario_id,
                "inquilino": None,
                "descripcion": "Hogar con ambiente familiar.",
                "estado": 1,
                "direccion": "Calle 30 #35-42",
                "comuna": 11,
                "canon_cop": 800000,
                "area_m2": 30,
                "piso": 1,
                "calificacion": 0,
                "estado_cambiado": True
            }
        }
        self.correct_response2: dict = {
            "id": 1,
            "usuario": self.arrendador.usuario_id,
            "inquilino": None,
            "descripcion": "Hogar con ambiente familiar.",
            "estado": 1,
            "direccion": "Calle 30 #35-42",
            "comuna": 11,
            "canon_cop": 800000,
            "area_m2": 30,
            "piso": 1,
            "estado_cambiado": True,
            "calificacion": 0,
            "imagenes": [
                {
                   "id": 1,
                   "publicacion_id": 1,
                   "data": "\xdeadbeef",
                   "fecha": datetime.date.today().strftime("%Y-%m-%d")
                 },
                 {
                   "id": 2,
                   "publicacion_id": 1,
                   "data": "\xdeaaxvhnj",
                   "fecha": datetime.date.today().strftime("%Y-%m-%d")
                 }
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
            loads(response.content),
            self.correct_response
        )

    def test_create_required_field(self):
        new_publicacion_data: dict = {
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

    def test_read_correct(self):
        Publicacion.objects.create(**self.publicacion_data)
        response = self.client.get(path="/publicacion/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            loads(response.content)[0],
            self.correct_response2
        )


class UpdateDeletePublicacionTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.arrendador = User.objects.create(
            nombre="Arrendador",
            correo="arrendador@unal.edu.co",
            celular="310495520",
            password="arrendador",
            rol=1
        )
        self.new_publicacion_data : dict = {
            "descripcion": "Habitación con ambiente familiar, wifi 500mbs, acceso a zonas comunes y parquedearo.",
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
        self.imagen: Imagen = Imagen.objects.create(
            publicacion=self.publicacion,
            data=bytes("\xdeadbeef", "UTF-8"),
        )
        self.correct_response: dict = {
            "id": self.publicacion.id,
            "usuario": self.arrendador.usuario_id,
            "inquilino": None,
            "descripcion": "Hogar con ambiente familiar.",
            "estado": 1,
            "direccion": "Calle 30 #35-42",
            "comuna": 11,
            "canon_cop": 800000,
            "area_m2": 30,
            "piso": 1,
            "calificacion": 8,
            "estado_cambiado": True,
            "imagenes": [
                {
                    "id": 1,
                    "publicacion": self.publicacion.id,
                    "data": "\xdeadbeef",
                    "fecha": datetime.date.today().strftime("%Y-%m-%d")
                },
            ]
        }
        self.client.login(correo=self.arrendador.correo, password="arrendador")

    def test_read_correct(self):
        response = self.client.get(
            path=f"/publicacion/listar/{self.arrendador.id}/",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            loads(response.content)[0],
            self.correct_response
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

