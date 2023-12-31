from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from json import loads

from ..models import User


class RegisterTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            "nombre": "Calypso",
            "correo": "calypso@unal.edu.co",
            "celular": "310495520",
            "password": "calypso"
        }

    def test_register_correct(self):
        response = self.client.post("/register/", self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.last().correo, self.user_data["correo"])

    def test_register_invalid_email(self):
        self.client.post("/register/", self.user_data, format="json")
        response = self.client.post("/register/", self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            loads(response.content),
            {
                "correo": [
                    "user with this correo already exists."
                ]
            }
        )

    def test_register_required_field(self):
        new_user_data = {
            "nombre": "Calypso",
            "celular": "310495520",
            "password": "calypso"
        }
        response = self.client.post("/register/", new_user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            loads(response.content),
            {
                "correo": [
                    "This field is required."
                ]
            }
        )


class LoginTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            nombre="Cassandra",
            correo="cassandra@unal.edu.co",
            celular="310495520",
            password="cassandra"
        )

        self.login_data = {
            "correo": self.user.correo,
            "password": "cassandra"
        }

    def test_login_correct(self):
        response = self.client.post(path="/login/", data=self.login_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            loads(response.content)["correo"],
            self.user.correo
        )

    def test_login_incorrect_credentials(self):
        invalid_login_data = {
            "correo": "cassandra@unal.edu.co",
            "password": "1234"
        }
        response = self.client.post(path="/login/", data=invalid_login_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            loads(response.content),
            {
                "non_field_errors": [
                    "Incorrect Credentials"
                ]
            }
        )

    def test_login_required_field(self):
        invalid_login_data = {
            "correo": "cassandra@unal.edu.co"
        }
        response = self.client.post(path="/login/", data=invalid_login_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            loads(response.content),
            {
                "password": [
                    "This field is required."
                ]
            }
        )


class DeleteUpdateUserTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            nombre="Cassandra",
            correo="cassandra@unal.edu.co",
            celular="310495520",
            password="cassandra"
        )
        self.new_data = {
            "tipo_documento": "CC",
            "documento": 1001031722,
            "validado": True,
            "rol": 2
        }

    def test_update_user_correct(self):
        response = self.client.patch(path=f"/usuario/{self.user.usuario_id}/", data=self.new_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            User.objects.last().rol,
            2
        )

    def test_update_user_nonexistent(self):
        response = self.client.patch(path="/usuario/100/", data=self.new_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            loads(response.content),
            {
                "message": "User does not exist"
            }
        )

    def test_update_field_nonexistent(self):
        invalid_data = {
            "nickname": "Cali",
            "tipo_documento": "CC",
            "documento": 1001031722,
            "validado": True,
            "rol": 2
        }
        response = self.client.patch(path=f"/usuario/{self.user.usuario_id}/", data=invalid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            loads(response.content),
            {
                "message": "nickname attribute does not exist"
            }
        )

    def test_delete_user_correct(self):
        response = self.client.delete(path=f"/usuario/{self.user.usuario_id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            User.objects.count(),
            0
        )

    def test_delete_user_nonexistent(self):
        response = self.client.delete(path="/usuario/100/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            loads(response.content),
            {
                "message": "User does not exist"

            }
        )

class LogoutTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            nombre="Calypso",
            correo="calyso@unal.edu.co",
            celular="310495520",
            password="calypso"
        )

        self.client.login(correo=self.user.correo, password="calypso")

    def test_logout_correct(self):
        response = self.client.post(path="/logout/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            loads(response.content),
            {"message": "User logged out successfully"}
        )

    def test_logout_unauthenticated(self):
        self.client.logout()
        response = self.client.post(path="/logout/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            loads(response.content),
            {
                "detail": "Authentication credentials were not provided."
            }
        )