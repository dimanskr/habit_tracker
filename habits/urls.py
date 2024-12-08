from rest_framework.routers import SimpleRouter
from django.urls import path

from habits.apps import HabitsConfig
from habits.views import HabitsViewSet, HabitsListAPIView

app_name = HabitsConfig.name

router = SimpleRouter()
router.register(r'habits', HabitsViewSet, basename='habits')

urlpatterns = [
                  path('public-habits/', HabitsListAPIView.as_view(), name='habits-list'),
              ] + router.urls
