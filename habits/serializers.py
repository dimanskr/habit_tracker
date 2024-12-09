from rest_framework import serializers

from habits.models import Habit
from habits.validators import (
    associated_habit_validator,
    exclude_simultaneous_associated_habit_reward_validator,
    execution_time_validator, period_validator,
    pleasurable_habit_cant_have_reward_or_associated_habit_validator)


class HabitSerializers(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"
        validators = [
            exclude_simultaneous_associated_habit_reward_validator,
            execution_time_validator,
            associated_habit_validator,
            pleasurable_habit_cant_have_reward_or_associated_habit_validator,
            period_validator,
        ]
