from django.db import models

NULLABLE = {"null": True, "blank": True}


class Habit(models.Model):
    action = models.CharField(max_length=150, verbose_name="действие")
    owner = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, verbose_name="создатель", **NULLABLE
    )
    place = models.CharField(max_length=150, verbose_name="место")
    time = models.DateTimeField(verbose_name="дата и время выполнения привычки")
    is_pleasurable = models.BooleanField(
        default=False, verbose_name="признак приятной привычки"
    )
    associated_habit = models.ForeignKey(
        "self", on_delete=models.SET_NULL, **NULLABLE, verbose_name="связанная привычка"
    )
    period = models.PositiveIntegerField(default=1, verbose_name="периодичность в днях")
    reward = models.CharField(max_length=150, verbose_name="вознаграждение", **NULLABLE)
    execution_time = models.TimeField(verbose_name="время на выполнение", **NULLABLE)
    is_public = models.BooleanField(default=True, verbose_name="признак публичности")

    def __str__(self):
        return f"Я буду {self.action} в {self.time} в {self.place}"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = ("time",)
