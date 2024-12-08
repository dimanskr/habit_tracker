from django.contrib import admin

from habits.models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "action",
        "place",
        "time",
        "is_pleasurable",
        "associated_habit",
        "period",
        "reward",
        "execution_time",
        "is_public",
    )
