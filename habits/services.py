import requests

from config.settings import TELEGRAM_TOKEN


def send_telegram_message(message, tg_chat_id):
    """Отправка сообщения в Telegram через бот"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": tg_chat_id, "text": message}
    requests.post(url, data=data)
