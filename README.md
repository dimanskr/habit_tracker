# Курсовая работа DFR

## Установка и запуск

1. Установите зависимости из файла `pyproject.toml`, используя Poetry:
    ``` bash
    poetry install
    ```
2. Создайте базу данных postgresql, пропишите настройки подключения к ней
в файле .env в корне проекта, а так же настройки CORS, CELERY 
и TELEGRAM_TOKEN для получения сообщений (его можно узнать в Telegram BotFather). 
([шаблон файла](.env.sample))


3. Примените миграции
   ``` bash
    python manage.py migrate
   ```

4. Создайте учетную запись администратора кастомной командой:
   ``` bash
   python manage.py csu
   ```
   *email: admin@mail.ru* \
   *пароль: 11111111*


5. Установите redis и запустите сервер redis:
   ``` bash
    sudo service redis-server start
   ```

7. Запустите Celery worker (для Windows с флагом `-P eventlet`) 
и celery-beat для периодических задач:
    ```bash
    celery -A config worker -l INFO -P eventlet
    celery -A config beat --loglevel=info
    ```
8. Запустите сервер:
    ```bash
    python manage.py runserver
    ```
На эндпоинте `/users/login/` получаем токен `access`,
 который нужно использовать для доступа к другим эндпоинтам. 

Через админку или эндпоинт `/users/update/` задайте пользователю 
`tg_chat_id` для получения сообщений в Telegram.


## Эндпоинты можно посмотреть в документации swagger или redoc


