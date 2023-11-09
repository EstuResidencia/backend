from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from json import loads

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
            "usuario": self.user.pk,
            "publicacion": self.publicacion.id,
        }

        # Realiza una solicitud POST para crear una solicitud
        response = self.client.post("/solicitud/", solicitud_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # 201 Creado
        solicitud = Solicitud.objects.get(id=loads(response.content)['solicitud']['id'])
        self.assertEqual(solicitud.estado, 1)  # Verifica que el estado sea PENDIENTE
        self.assertEqual(solicitud.pagado, False)  # Verifica que pagado sea False

    def test_create_solicitud_invalid_data(self):
        # Datos de solicitud con campos faltantes
        solicitud_data = {}

        # Realiza una solicitud POST con datos incompletos
        response = self.client.post("/solicitud/", solicitud_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  # 400 Bad Request

    def test_create_solicitud_not_found(self):
        # Intenta crear una solicitud para una publicación inexistente (publicacion_id)
        solicitud_data = {
            "usuario": self.user.pk,
            "publicacion": 999,  # ID inexistente
        }

        response = self.client.post("/solicitud/", solicitud_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  # 400 Bad Request

    def test_create_solicitud_existing_solicitud(self):
        # Intenta crear una solicitud duplicada
        solicitud_data = {
            "usuario": self.user.pk,
            "publicacion": self.publicacion.id,
        }

        # Crea una solicitud inicialmente
        response1 = self.client.post("/solicitud/", solicitud_data, format='json')

        self.assertEqual(response1.status_code, 201)  # 201 Creado

        # Intenta crear la misma solicitud nuevamente
        response2 = self.client.post("/solicitud/", solicitud_data, format='json')

        self.assertEqual(response2.status_code, 400)  # 400 Bad Request


class ReadUpdateDeleteSolicitudTestCase(TestCase):
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
        # Crear una solicitud de ejemplo para las pruebas
        self.solicitud = Solicitud.objects.create(
            usuario=self.user,
            publicacion=self.publicacion,
        )

    # GET
    def test_get_solicitud_correct(self):
        # Realiza una solicitud GET para obtener los detalles de la solicitud creada
        response = self.client.get(f"/solicitud/{self.solicitud.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)  # 200 OK
        self.assertEqual(loads(response.content)['usuario'], self.user.pk)  # Verifica los detalles de la solicitud

    def test_get_solicitud_not_found(self):
        # Intenta obtener detalles de una solicitud inexistente
        response = self.client.get("/solicitud/999/")  # ID inexistente

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)  # 404 Not Found
        self.assertEqual(loads(response.content)['message'], "Solicitud no existe")

    # PATCH
    def test_update_solicitud_correct(self):
        # Datos de ejemplo para la solicitud PATCH
        updated_data = {
            "estado": 2,
            "pagado": True,
        }

        # Realiza una solicitud PATCH para actualizar la solicitud
        response = self.client.patch(f"/solicitud/{self.solicitud.id}/", updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)  # 200 OK
        self.assertEqual(loads(response.content)['solicitud']['estado'], 2)  # Verifica el estado actualizado
        self.assertEqual(loads(response.content)['solicitud']['pagado'], True)  # Verifica pagado actualizado

    def test_update_solicitud_not_found(self):
        # Intenta actualizar una solicitud que no existe
        updated_data = {
            "estado": 2,
            "pagado": True,
        }

        response = self.client.patch("/solicitud/999/", updated_data, format='json')  # ID inexistente

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)  # 404 Not Found
        self.assertEqual(loads(response.content)['message'], "Solicitud no existe")

    # DELETE

    def test_delete_solicitud_correct(self):
        # Realiza una solicitud DELETE para eliminar la solicitud
        response = self.client.delete(f"/solicitud/{self.solicitud.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)  # 200 OK
        self.assertEqual(loads(response.content)['message'], "Solicitud fue eliminada exitosamente")
        with self.assertRaises(Solicitud.DoesNotExist):
            self.solicitud.refresh_from_db()

    def test_delete_solicitud_not_found(self):
        # Intenta eliminar una solicitud que no existe
        response = self.client.delete("/solicitud/999/")  # ID inexistente

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)  # 404 Not Found
        self.assertEqual(loads(response.content)['message'], "Solicitud no existe")


class ListSolicitudByEstudianteTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            nombre="Calypso",
            correo="calypso@unal.edu.co",
            celular="310495520",
            password="calypso"
        )
        self.client.force_authenticate(self.user)

        # Crear una solicitud de ejemplo para las pruebas
        self.publicacion = Publicacion.objects.create(
            usuario=self.user,
            descripcion="Publicacion de prueba",
            direccion="Calle 123",
            canon_cop=1000000,
            area_m2=100,
            piso=1,
            comuna=1
        )
        self.solicitud = Solicitud.objects.create(
            usuario=self.user,
            publicacion=self.publicacion,
            estado=2  # Estado 2 para simular una solicitud diferente
        )

    def test_get_solicitudes_estudiante_correct(self):
        # Realiza una solicitud GET para obtener todas las solicitudes asociadas al estudiante (usuario)
        response = self.client.get(f"/solicitud/estudiante/{self.user.pk}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)  # 200 OK
        self.assertTrue(len(loads(response.content)) > 0)  # Verifica que al menos una solicitud se haya devuelto

    def test_get_solicitudes_estudiante_not_found(self):
        # Intenta obtener solicitudes para un estudiante (usuario) inexistente
        response = self.client.get("/solicitud/estudiante/999/")  # ID de estudiante inexistente

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)  # 404 Not Found
        self.assertEqual(loads(response.content)['message'], "Estudiante no existe")


class ListSolicitudByArrendadorTestCase(TestCase):
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

        # Crear una solicitud de ejemplo para las pruebas
        self.publicacion = Publicacion.objects.create(
            usuario=self.arrendador,
            descripcion="Publicacion de prueba",
            direccion="Calle 123",
            canon_cop=1000000,
            area_m2=100,
            piso=1,
            comuna=1
        )
        self.solicitud = Solicitud.objects.create(
            usuario=self.user,
            publicacion=self.publicacion,
            estado=1  # Estado 1 para simular una solicitud diferente
        )

    def test_get_solicitudes_arrendador_correct(self):
        # Realiza un GET para obtener todas las solicitudes asociadas a todas las publicaciones del arrendador
        response = self.client.get(f"/solicitud/arrendador/{self.arrendador.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)  # 200 OK
        self.assertTrue(len(loads(response.content)) > 0)  # Verifica que al menos una solicitud se haya devuelto

    def test_get_solicitudes_arrendador_not_found(self):
        # Intenta obtener solicitudes para un arrendador inexistente
        response = self.client.get("/solicitud/arrendador/999/")  # ID de arrendador inexistente

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)  # 404 Not Found
        self.assertEqual(loads(response.content)['message'], "Arrendador no existe")
