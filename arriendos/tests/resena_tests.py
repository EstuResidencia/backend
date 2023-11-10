import datetime

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from json import loads

from accounts.models import User
from ..models import Solicitud, Resena
from ..models.imagen import Imagen
from ..models.publicacion import Publicacion


class CreateReadResenaTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.resenador: User = User.objects.create(
            nombre="Frito en Brito",
            correo="testCorreo@universidad.edu.co",
            password="testPassword",
            celular="3018495438",
            documento="100056789",
            tipo_documento="CC",
                )
        self.resenador_2: User = User.objects.create(
                nombre="Emigdio Resenador",
                correo="eporrasm@unal.edu.co",
                password="ayelmao",
                celular="3018495438",
                documento="1001056789",
                tipo_documento="CC",
                )
        self.arrendador: User = User.objects.create(
            nombre="Emigdio Arrendador",
            correo="elMejorArrendador@gmail.com",
            password="arriendos123",
            celular="3108374856",
            documento="123456789",
            tipo_documento="CC",
                )
        self.publicacion: Publicacion = Publicacion.objects.create(
                usuario=self.arrendador,
                descripcion="Habitación cómoda para estudiante.",
                direccion="Calle 20 #35-42",
                comuna=4,
                canon_cop=650000,
                area_m2=25,
                piso=1
                )
        self.resena_creada = Resena.objects.create(
                usuario=self.resenador,
                publicacion=self.publicacion,
                comentario="Interesante habitación.",
                calificacion=7,
                )

        self.resena_correcta: dict = {
                "usuario": self.resenador.pk,
                "comentario": "Muy buena habitación, muy agradable.",
                "calificacion": 9,
                }
        self.resena_correcta_2: dict = {
                "usuario": self.resenador_2.pk,
                "comentario": "",
                "calificacion": 8,
                }

        self.client.login(correo=self.resenador.correo, password="testPassword")

    def test_create_resena_correct(self):
        response = self.client.post(path=f"/resena/{self.publicacion.id}/", data=self.resena_correcta)
        self.client.logout()
        self.client.login(correo=self.resenador_2.correo, password="ayelmao")
        response2 = self.client.post(path=f"/resena/{self.publicacion.id}/", data=self.resena_correcta_2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.publicacion.resenas.count(), 3)
        self.assertEqual(datetime.date.today(), self.publicacion.resenas.first().fecha)

    def test_read_resenas_correct(self):
        response = self.client.get(path=f"/resena/{self.publicacion.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(loads(response.content)), 1)

    def test_read_resenas_incorrect(self):
        response = self.client.get(path=f"/resena/100/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(loads(response.content)["message"], "La publicación no existe")


class NotificationSignalTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user: User = User.objects.create(
                nombre="Emigdio Resenador",
                correo="eporrasm@unal.edu.co",
                password="ayelmao",
                celular="3018495438",
                documento="1001056789",
                tipo_documento="CC",
                )
        self.publicacion_1: Publicacion = Publicacion.objects.create(
                usuario=self.user,
                descripcion="Habitación cómoda para estudiante.",
                direccion="Calle 20 #35-42",
                comuna=4,
                canon_cop=650000,
                area_m2=25,
                piso=1
                )
        self.publicacion_2: Publicacion = Publicacion.objects.create(
                usuario=self.user,
                descripcion="Lugar agradable y en un piso alto.",
                direccion="Calle 30 #35-42",
                comuna=12,
                canon_cop=850000,
                area_m2=35,
                piso=19
                )
        self.imagen_1: Imagen  = Imagen.objects.create(
                publicacion=self.publicacion_2,
                data=bytes("aaxvhnj", "UTF-8"),
                )
        self.imagen_2: Imagen  = Imagen.objects.create(
                publicacion=self.publicacion_2,
                data=bytes("\xde\xaa\xbaxv", "UTF-8"),
                )

        self.solicitud: Solicitud = Solicitud.objects.create(
                usuario=self.user,
                publicacion=self.publicacion_2,
                )

        self.return_correct_dict: dict = {
                "publicaciones":[
                        {
                            "id": self.publicacion_2.pk,
                            "usuario": self.user.pk,
                            "inquilino": None,
                            "descripcion": "Lugar agradable y en un piso alto.",
                            "estado": 1,
                            "direccion": "Calle 30 #35-42",
                            "comuna": 12,
                            "canon_cop": 850000,
                            "area_m2": 35,
                            "piso": 19,
                            "calificacion": 8,
                            "estado_cambiado": True,
                            "imagenes": [
                                    {
                                        "id": self.imagen_1.id,
                                        "publicacion": self.publicacion_2.pk,
                                        "data": "aaxvhnj",
                                        "fecha": datetime.date.today().strftime("%Y-%m-%d")
                                    },
                                    {
                                        "id": self.imagen_2.id,
                                        "publicacion": self.publicacion_2.pk,
                                        "data": "\xde\xaa\xbaxv",
                                        "fecha": datetime.date.today().strftime("%Y-%m-%d")
                                    }
                            ]
                        }
                ],
                "solicitudes":[
                        {
                            "id": self.solicitud.pk,
                            "usuario": self.user.pk,
                            "publicacion": self.publicacion_2.pk,
                            "estado": 1,
                            "pagado": False,
                            "fecha": datetime.date.today().strftime("%Y-%m-%d"),
                            "estado_cambiado": True
                        }
                ]
        }

        self.resena_creada: Resena = Resena.objects.create(
                usuario=self.user,
                publicacion=self.publicacion_2,
                comentario="Interesante habitación.",
                calificacion=8,
                )
        self.resena_creada_2: Resena = Resena.objects.create(
                usuario=self.user,
                publicacion=self.publicacion_2,
                comentario="Interesante habitación.",
                calificacion=9,
                )
        # self.maxDiff = None

    def test_get_notification_signal_data(self):
        self.publicacion_1.estado_cambiado = False
        self.publicacion_1.save()

        response = self.client.get(path=f"/notification-signal/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(loads(response.content), self.return_correct_dict)
