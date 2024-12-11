from rest_framework import generics, viewsets

from habits.models import Habit
from habits.paginators import HabitPagination
from habits.serializers import HabitSerializers
from users.permissions import IsOwner


class HabitsViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializers
    pagination_class = HabitPagination

    def perform_create(self, serializer):
        """Сохраняет новому объекту владельца"""
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        """
        Права пользователей с привычками
        """
        if self.action in ["retrieve", "update", "partial_update", "destroy"]:
            # доступ к привычкам только владельцу
            self.permission_classes = (IsOwner,)
        return super().get_permissions()

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Habit.objects.filter(owner=user)
        return Habit.objects.none()


class HabitsListAPIView(generics.ListAPIView):
    serializer_class = HabitSerializers
    pagination_class = HabitPagination

    def get_queryset(self):
        """
        Вывод только публичных привычек
        """
        queryset = Habit.objects.filter(is_public=True)
        return queryset
