from django.db import models

NULLABLE = {"null": True, "blank": True}


class Habit(models.Model):
    name = models.CharField(max_length=150, verbose_name="название")
    owner = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, verbose_name="создатель", **NULLABLE
    )
    place = models.CharField(max_length=150, verbose_name="место")
    time = models.TimeField(verbose_name="время")
    action = models.CharField(max_length=150, verbose_name="действие")
    is_pleasurable = models.BooleanField(
        default=False, verbose_name="признак приятной привычки"
    )
    associated_habit = models.ForeignKey(
        "self", on_delete=models.SET_NULL, **NULLABLE, verbose_name="связанная привычка"
    )
    period = models.IntegerField(default=1, verbose_name="периодичность в днях")
    reward = models.CharField(max_length=150, verbose_name="вознаграждение", **NULLABLE)
    execution_time = models.TimeField(verbose_name="время на выполнение", **NULLABLE)
    is_public = models.BooleanField(default=True, verbose_name="признак публичности")

    def __str__(self):
        return f"Я буду {self.name} в {self.time} в {self.place}"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
