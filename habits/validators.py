from datetime import time

from rest_framework import serializers


def exclude_simultaneous_associated_habit_reward_validator(value):
    """Исключить одновременный выбор связанной привычки и указания вознаграждения"""
    if value.get("associated_habit") and value.get("reward"):
        raise serializers.ValidationError(
            "Исключить одновременный выбор связанной привычки и указания вознаграждения."
        )


def execution_time_validator(value):
    """Время выполнения должно быть не больше 120 секунд"""
    if value.get("execution_time") and value.get("execution_time") > time(00, 2):
        raise serializers.ValidationError(
            "Время выполнения должно быть не больше 120 секунд."
        )


def associated_habit_validator(value):
    """В связанные привычки могут попадать только приятные привычки"""
    if (
        value.get("associated_habit")
        and not value.get("associated_habit").is_pleasurable
    ):
        raise serializers.ValidationError(
            "В связанные привычки могут попадать только привычки с признаком приятной привычки."
        )


def pleasurable_habit_cant_have_reward_or_associated_habit_validator(value):
    """У приятной привычки не может быть вознаграждения или связанной привычки"""
    if value.get("is_pleasurable") and (
        value.get("associated_habit") or value.get("reward")
    ):
        raise serializers.ValidationError(
            "У приятной привычки не может быть вознаграждения или связанной привычки."
        )


def period_validator(value):
    """Нельзя выполнять привычку реже, чем 1 раз в 7 дней"""
    if value.get("period") and value.get("period") > 7:
        raise serializers.ValidationError(
            "Нельзя выполнять привычку реже, чем 1 раз в 7 дней."
        )
