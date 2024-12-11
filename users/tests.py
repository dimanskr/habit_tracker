from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UserTests(APITestCase):
    def setUp(self):
        # Создаем пользователя
        self.user1 = User.objects.create_user(
            email="user1@example.com", password="password1"
        )
        self.user2 = User.objects.create_user(
            email="user2@example.com", password="password2"
        )
        self.client.force_authenticate(user=self.user1)

    def test_create_user(self):
        """
        Тест создания нового пользователя
        """
        data = {
            "email": "newuser@example.com",
            "password": "newpassword",
        }
        response = self.client.post(reverse("users:user-register"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)

    def test_retrieve_own_profile(self):
        """
        Тест получения данных собственного профиля
        """
        url = reverse("users:user-profile", args=[self.user1.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "user1@example.com")

    def test_retrieve_other_user_profile(self):
        """
        Тест попытки получения чужого профиля
        """
        url = reverse("users:user-profile", args=[self.user2.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_own_profile(self):
        """
        Тест обновления собственного профиля
        """
        data = {
            "tg_chat_id": "123456789",
        }
        url = reverse("users:user-profile", args=[self.user1.pk])
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["tg_chat_id"], "123456789")

    def test_update_other_user_profile(self):
        """
        Тест попытки обновления чужого профиля
        """
        data = {
            "tg_chat_id": "123456789",
        }
        url = reverse("users:user-profile", args=[self.user2.pk])
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
