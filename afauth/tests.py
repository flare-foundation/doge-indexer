from django.urls import reverse
from rest_framework.test import APITestCase

from .models import AFUser


class TestAuthentication(APITestCase):
    def setUp(self) -> None:
        self.usr = AFUser.objects.create_user("tester@aflabs.si", "Testing", "user", "password")

        self.users: list[AFUser] = []

    def test_jwt_token_authentication(self) -> None:
        unauthenticated = self.client.get(reverse("token-login"))
        self.assertEqual(unauthenticated.status_code, 405)

        auth = self.client.post(
            reverse("token-login"),
            data={"email": self.usr.email, "password": "password"},
        )

        self.assertEqual(auth.status_code, 200)
        self.assertIsInstance(auth.json()["refresh"], str)
        self.assertIsInstance(auth.json()["access"], str)

    def test_jwt_token_refresh(self) -> None:
        auth = self.client.post(  # just to get valid token
            reverse("token-login"),
            data={"email": self.usr.email, "password": "password"},
        )
        self.assertEqual(auth.status_code, 200)
        refresh_valid = self.client.post(reverse("token-refresh"), data={"refresh": auth.json()["refresh"]})
        self.assertEqual(refresh_valid.status_code, 200)
        self.assertIsInstance(auth.json()["access"], str)


class TestAuthenticated(APITestCase):
    def setUp(self) -> None:
        self.usr = AFUser.objects.create_user("tester@aflabs.si", "Testing", "user", "password")

        auth = self.client.post(
            reverse("token-login"),
            data={"email": self.usr.email, "password": "password"},
        )
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + auth.json()["access"])
        self.users: list[AFUser] = []

    def test_users_me(self) -> None:
        me = self.client.get("/api/auth/user")
        self.assertEqual(me.status_code, 200)
