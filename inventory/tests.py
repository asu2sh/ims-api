from django.contrib.auth.models import User
from django.urls import reverse

from .models import Item

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken


class ItemViewTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.token = str(AccessToken.for_user(self.user))
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

        self.item = Item.objects.create(
            name="Test Item", description="A test item", quantity=10
        )
        self.item_url = reverse("item_detail", kwargs={"item_id": self.item.id})

    def test_register_user(self):
        url = reverse("register_user")
        data = {
            "username": "newuser",
            "password": "newpass123",
            "password2": "newpass123",
            "email": "newuser@example.com",
            "first_name": "New",
            "last_name": "User",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(
            User.objects.get(username="newuser").email, "newuser@example.com"
        )

    def test_register_user_password_mismatch(self):
        url = reverse("register_user")
        data = {
            "username": "newuser",
            "password": "newpass123",
            "password2": "wrongpass",
            "email": "newuser@example.com",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)

    def test_token_obtain_pair(self):
        url = reverse("token_obtain_pair")
        data = {"username": "testuser", "password": "testpass"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_token_obtain_pair_invalid_credentials(self):
        url = reverse("token_obtain_pair")
        data = {"username": "wronguser", "password": "wrongpass"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("No active account", response.data["detail"])

    def test_token_refresh(self):
        url_obtain = reverse("token_obtain_pair")
        url_refresh = reverse("token_refresh")

        data = {"username": "testuser", "password": "testpass"}
        response = self.client.post(url_obtain, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        refresh_token = response.data["refresh"]

        data = {"refresh": refresh_token}
        response = self.client.post(url_refresh, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_token_refresh_invalid_token(self):
        url = reverse("token_refresh")
        data = {"refresh": "invalidtoken"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("Token is invalid", response.data["detail"])

    def test_get_item(self):
        response = self.client.get(self.item_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Test Item")
        self.assertEqual(response.data["quantity"], 10)

    def test_create_item(self):
        data = {
            "name": "New Item",
            "description": "New item description",
            "quantity": 5,
        }
        response = self.client.post(reverse("item_list"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Item.objects.count(), 2)
        self.assertEqual(response.data["name"], "New Item")

    def test_update_item_quantity(self):
        data = {"name": "Test Item", "description": "A test item", "quantity": 20}
        response = self.client.put(self.item_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.item.refresh_from_db()
        self.assertEqual(self.item.quantity, 20)

    def test_delete_item(self):
        response = self.client.delete(self.item_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Item.objects.count(), 0)
