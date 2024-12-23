import datetime

from celery import shared_task
from django.utils import timezone

from habits.models import Habit
from habits.services import send_telegram_message


@shared_task
def send_habits():
    """
    Задача отправки напоминаний о привычках
    """
    # выбираем текущую дату и время
    current_datetime = datetime.datetime.now()
    # Получаем привычки по указанным в фильтре параметрам
    habits = Habit.objects.filter(
        owner__tg_chat_id__isnull=False,  # Убедимся, что Telegram ID у владельца указан
        time__date=current_datetime.date(),  # Привычки на сегодня
        time__hour=current_datetime.hour,  # Совпадение по часу
        time__minute=current_datetime.minute,  # Совпадение по минуте
    )
    for habit in habits:
        local_time = timezone.localtime(habit.time)
        formatted_time = local_time.strftime("%H:%M")
        message = f"Напоминание о привычке '{habit.action}' в '{habit.place}' в {formatted_time}."
        # отправляем привычку в телеграм
        send_telegram_message(message, habit.owner.tg_chat_id)
        # изменяем дату привычки
        habit.time += datetime.timedelta(days=habit.period)
        habit.save()
