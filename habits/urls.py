from django.urls import path
from rest_framework.routers import SimpleRouter

from habits.apps import HabitsConfig
from habits.views import HabitsListAPIView, HabitsViewSet

app_name = HabitsConfig.name

router = SimpleRouter()
router.register(r"habits", HabitsViewSet, basename="habits")

urlpatterns = [
    path("public-habits/", HabitsListAPIView.as_view(), name="habits-public"),
] + router.urls
