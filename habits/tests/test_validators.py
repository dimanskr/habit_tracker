import unittest
from datetime import time

from rest_framework.exceptions import ValidationError

from habits.serializers import (
    associated_habit_validator,
    exclude_simultaneous_associated_habit_reward_validator,
    execution_time_validator, period_validator,
    pleasurable_habit_cant_have_reward_or_associated_habit_validator)


class TestValidators(unittest.TestCase):

    def test_exclude_simultaneous_associated_habit_reward_validator_with_both(self):
        data = {"associated_habit": True, "reward": "reward"}
        with self.assertRaises(ValidationError) as cm:
            exclude_simultaneous_associated_habit_reward_validator(data)
        self.assertTrue(
            "Исключить одновременный выбор связанной привычки и указания вознаграждения"
            in str(cm.exception),
            "Unexpected validation error message.",
        )

    def test_exclude_simultaneous_associated_habit_reward_validator_without_both(self):
        data = {"associated_habit": True, "reward": ""}
        # Не вызывает ошибку
        exclude_simultaneous_associated_habit_reward_validator(data)

    def test_execution_time_validator_with_invalid_time(self):
        data = {"execution_time": time(0, 3)}
        with self.assertRaises(ValidationError) as cm:
            execution_time_validator(data)
        self.assertTrue(
            "Время выполнения должно быть не больше 120 секунд" in str(cm.exception),
            "Unexpected validation error message.",
        )

    def test_execution_time_validator_with_valid_time(self):
        data = {"execution_time": time(0, 1)}
        # Не вызывает ошибку
        execution_time_validator(data)

    def test_associated_habit_validator_with_non_pleasurable(self):
        associated_habit = type("Habit", (object,), {"is_pleasurable": False})()
        data = {"associated_habit": associated_habit}
        with self.assertRaises(ValidationError) as cm:
            associated_habit_validator(data)
        self.assertTrue(
            "признаком приятной привычки" in str(cm.exception),
            "Unexpected validation error message.",
        )

    def test_associated_habit_validator_with_pleasurable(self):
        associated_habit = type("Habit", (object,), {"is_pleasurable": True})()
        data = {"associated_habit": associated_habit}
        # Не вызывает ошибку
        associated_habit_validator(data)

    def test_pleasurable_habit_cant_have_reward_or_associated_habit_validator_with_both(
        self,
    ):
        data = {"is_pleasurable": True, "associated_habit": True, "reward": "reward"}
        with self.assertRaises(ValidationError) as cm:
            pleasurable_habit_cant_have_reward_or_associated_habit_validator(data)
        self.assertTrue(
            "не может быть вознаграждения или связанной привычки" in str(cm.exception),
            "Unexpected validation error message.",
        )

    def test_pleasurable_habit_cant_have_reward_or_associated_habit_validator_without_both(
        self,
    ):
        data = {"is_pleasurable": True, "associated_habit": False, "reward": ""}
        # Не вызывает ошибку
        pleasurable_habit_cant_have_reward_or_associated_habit_validator(data)

    def test_period_validator_with_invalid_period(self):
        data = {"period": 8}
        with self.assertRaises(ValidationError) as cm:
            period_validator(data)
        self.assertTrue(
            "реже, чем 1 раз в 7 дней" in str(cm.exception),
            "Unexpected validation error message.",
        )

    def test_period_validator_with_valid_period(self):
        data = {"period": 7}
        # Не вызывает ошибку
        period_validator(data)
