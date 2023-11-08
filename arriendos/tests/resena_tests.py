import datetime

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from json import loads

from accounts.models import User
from ..models.resena import Resena
from ..models.publicacion import Publicacion


class CreateReadResenaTestCase(TestCase):
    def setUpClass(self):
        self.client = APIClient()
        self.resenador = User.objects.create_user(
            nombre="Frito en Brito",
            correo="testCorreo@universidad.edu.co",
            password="testPassword",
            celular="3018495438",
            documento="100056789",
            tipo_documento="CC",
                )
        self.resenador_2 = User.objects.create_user(
                nombre="Emigdio Resenador",
                correo="eporrasm@unal.edu.co",
                password="ayelmao",
                celular="3018495438",
                documento="100056789",
                tipo_documento="CC",
                )
        self.arrendador = User.objects.create(
            nombre="Emigdio Arrendador",
            correo="elMejorArrendador@gmail.com",
            password="arriendos123",
            celular="3108374856",
            documento="123456789",
            tipo_documento="CC",
                )
        self.publicacion = Publicacion.objects.create(
                usuario=self.arrendador.id,
                descripcion="Habitación cómoda para estudiante.",
                direccion="Calle 20 #35-42",
                comuna=4,
                canon_cop=650000,
                area_m2=25,
                piso=1
                )
        self.resena_correcta = {
                "usuario": self.resenador.id,
                "comentario": "Muy buena habitación, muy agradable.",
                "calificacion": 9,
                }
        self.resena_correcta_2 = {
                "usuario": self.resenador_2.id,
                "comentario": "",
                "calificacion": 8,
                }

        self.client.login(correo=self.resenador.correo, password="testPassword")

    def test_create_publicacion_correct(self):
        response = self.client.post(path=f"/resena/{self.publicacion.id}/", data=self.resena_correcta)
        self.client.logout()
        self.client.login(correo=self.resenador_2.correo, password="ayelmao")
        response2 = self.client.post(path=f"/resena/{self.publicacion.id}/", data=self.resena_correcta_2)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Publicacion.resenas.count(), 2)
        self.assertEqual(datetime.date.today().strftime("%Y-%m-%d"), Publicacion.resenas.first().fecha)

    def test_read_resenas_correct(self):
        response = self.client.get(path=f"/resena/{self.publicacion.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(loads(response.content)), 2)

    def test_read_resenas_incorrect(self):
        response = self.client.get(path=f"/resena/100/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(loads(response.content)["message"], "La publicación no existe")

    # def test_create_publicacion_incorrect(self):
    #     # No encuentra la publicacion
    #     response = self.client.post(path=f"/resena/{self.publicacion.id}/", data=self.resena_incorrecta)
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    #     self.assertEqual(loads(response.content)["message"], "El usuario no existe")


