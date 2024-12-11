import datetime

from celery import shared_task
from telegram import Bot

from config.settings import TELEGRAM_TOKEN
from habits.models import Habit

bot = Bot(token=TELEGRAM_TOKEN)


@shared_task
def send_telegram_message(text, chat_id):
    """
    Отправляет сообщение через Telegram.
    """
    try:
        bot.send_message(chat_id=chat_id, text=text)
    except Exception as e:
        print(f"Ошибка отправки сообщения в Telegram: {e}")


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
        message = f"Напоминание о привычке '{habit.action}' в '{habit.place}' в {habit.time.strftime('%H:%M')}."
        # отправляем привычку в телеграм как отложенную задачу Celery
        send_telegram_message.delay(message, habit.owner.tg_chat_id)
        # изменяем дату привычки
        habit.time += datetime.timedelta(days=habit.period)
        habit.save()
