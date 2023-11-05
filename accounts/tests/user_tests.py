from django.test import TestCase
from rest_framework.test import APIClient, RequestsClient
from rest_framework import status
from json import loads

from ..models import User


# TODO: fix login and logout tests
class RegisterTestCase(TestCase):

    def setUp(self):
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

        self.user = User.objects.create(
            nombre="Cassandra",
            correo="cassandra@unal.edu.co",
            celular="310495520",
            password="cassandra"
        )

        self.login_data = {
            "correo": self.user.correo,
            "password": self.user.password
        }

    def test_login_correct(self):
        user = User.objects.last()
        print(f"correo: {user.correo}\npassword: {user.password}",)
        response = self.client.post(path="/login/", data=self.login_data, format="json")
        print(response.content)
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


class LogoutTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            nombre="Calypso",
            correo="calyso@unal.edu.co",
            celular="310495520",
            password="calypso"
        )
        # self.client.login(correo=self.user.correo, password=self.user.password)
        self.csrf_token = self.client.login(correo=self.user.correo, password=self.user.password)
        # self.csrf_token = self.client.cookies["csrftoken"]


    def test_logout_correct(self):
        print("csrf_token: ", self.csrf_token)
        response = self.client.post(path="/logout/")
        print(response.content)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(
        #     loads(response.content),
        #     {"message": "User logged out successfully"}
        # )
