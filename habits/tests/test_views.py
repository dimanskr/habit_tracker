from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from users.models import User


class HabitTests(APITestCase):
    def setUp(self):
        # Создаём пользователей
        self.user = User.objects.create_user(
            email="user1@mail.ru", password="password1"
        )
        self.owner = User.objects.create_user(
            email="user2@mail.ru", password="password2"
        )

        # Создаём привычки для пользователей
        self.habit1 = Habit.objects.create(
            action="Читать книги",
            owner=self.user,
            place="Дом",
            time="2024-12-11T12:00:00Z",
            is_public=True,
        )
        self.habit2 = Habit.objects.create(
            action="Бегать",
            owner=self.owner,
            place="Парк",
            time="2024-12-12T07:00:00Z",
            is_public=False,
        )
        self.client.force_authenticate(user=self.owner)

    def test_list_public_habits(self):
        """
        Проверяем доступ ко всем публичным привычкам через HabitsListAPIView
        """
        response = self.client.get(reverse("habits:habits-public"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["action"], "Читать книги")
        self.assertEqual(response.data["results"][0]["is_public"], True)

    def test_list_owner_habits(self):
        """
        Проверяем доступ к списку своих привычек
        """
        response = self.client.get(reverse("habits:habits-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["action"], "Бегать")

    def test_get_habit_owner_user(self):
        """
        Проверяем доступ к своей привычке авторизованным пользователем
        """
        url = reverse("habits:habits-detail", args=[self.habit2.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["action"], "Бегать")

    def test_get_habit_other_user(self):
        """
        Проверяем доступ к чужой привычке авторизованным пользователем
        """
        url = reverse("habits:habits-detail", args=[self.habit1.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_habit(self):
        """
        Проверяем создание привычки авторизованным пользователем
        """
        data = {
            "action": "Медитировать",
            "place": "Дом",
            "time": "2024-12-15T06:30:00Z",
            "is_public": True,
        }
        response = self.client.post(reverse("habits:habits-list"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["action"], "Медитировать")
        self.assertEqual(Habit.objects.count(), 3)

    def test_update_habit_owner(self):
        """
        Проверяем, что пользователь может изменить свою привычку
        """
        data = {"action": "Новое действие"}
        url = reverse("habits:habits-detail", args=[self.habit2.pk])
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["action"], "Новое действие")

    def test_update_habit_not_owner(self):
        """
        Проверяем, что пользователь не может изменить чужую привычку
        """
        data = {"action": "Новое действие"}
        url = reverse("habits:habits-detail", args=[self.habit1.pk])
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_habit_owner(self):
        """
        Проверяем удаление привычки владельцем
        """
        url = reverse("habits:habits-detail", args=[self.habit2.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.count(), 1)

    def test_delete_habit_not_owner(self):
        """
        Проверяем, что пользователь не может удалить чужую привычку
        """
        url = reverse("habits:habits-detail", args=[self.habit1.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
