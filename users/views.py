from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny

from users.models import User
from users.serializers import UserSerializer


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer

    def perform_update(self, serializer):
        # Разрешаем редактирование только владельцу профиля
        if self.request.user != self.get_object():
            raise PermissionDenied("Вы можете редактировать только свой профиль.")
        # Сохраняем обновленные данные пользователя
        user = serializer.save()

        # Хэшируем пароль, если он передан
        if "password" in serializer.validated_data:
            user.set_password(serializer.validated_data["password"])
            user.save()

    def get_queryset(self):
        """
        Возвращает только профиль текущего пользователя.
        """
        if not self.request.user.is_authenticated:
            raise PermissionDenied("Вы должны быть авторизованы для доступа к профилю.")
        # Ограничиваем queryset текущим пользователем
        return User.objects.filter(pk=self.request.user.pk)
