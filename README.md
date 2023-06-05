# klogger

Простой сервис для сбора логов с системой пользователей, группами логов и т.д. Может отсылать `WARNING`, `ERROR` и `CRITICAL` логи в телеграм ([см. Планируемые фичи](https://github.com/konnovK/klogger#%D0%BF%D0%BB%D0%B0%D0%BD%D0%B8%D1%80%D1%83%D0%B5%D0%BC%D1%8B%D0%B5-%D1%84%D0%B8%D1%87%D0%B8)).

При запуске на сервере с адресом `<URL>`:

- __REST API__: Swagger API Docs доступна по адресу `<URL>/docs`

- __Админка__: доступна по адресу `<URL>/admin`

## Использование

1) Создать пользователя

2) Создать группу логов (группы логов принадлежат пользователям)

3) Писать логи в эту группу

## Запуск

__Для локального запуска__ необходимо передать переменные окружения (можно через `.env` файл):

- `DB_USER` - имя пользователя бд
- `DB_PASSWORD` - пароль пользователя бд
- `DB_HOST` - адрес сервера бд
- `DB_PORT` - порт сервера бд
- `DB_NAME` - название бд
- `ADMIN_EMAIL` - _(опционально)_ _(по умолчанию - `admin@example.com`)_ email для доступа в админку
- `ADMIN_PASSWORD` - _(опционально)_ _(по умолчанию - `123`)_ пароль для доступа в админку
- `TELEGRAM_TOKEN` - _(опционально)_ токен telegram бота, который будет слать логи в телеграм
- `TELEGRAM_USERS_IDS` - _(опционально)_ id пользователей, которым бот будет слать логи в телеграм

Далее необходимо выполнить команды:

```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python main.py
```

__Для запуска через `docker compose`__ необходимо передать эти же переменные окружения (можно через `.env` файл), и затем выполнить команду:

```bash
docker compose up -d
```

После выполнения этой команды запустятся контейнеры с приложением и бд (с авто перезапуском при рестарте машины), и создастся `volumes` с логом сервера и данными БД.

__Для запуска `docker` образа__ выполните `docker build --tag klogger .` и `docker run klogger`, передав через `-e` перечисленные ранее переменные окружения.

## Планируемые фичи

- клиент (браузерный)
- миграции (скоро прикручу)
- тесты (!!!)
- Вынести в переменные окружения типы логов, которые может посылать тг бот

## Сущности

### LogGroup

Логи группируются по группам. У группы есть владелец. Писать логи в группу может только владелец. Владелец группы - это тот пользователь, кто эту группу создал.

### LogItem

Сообщение логгера. Имеет группу, которой пренадлежит. Писать логи в группу может только владелец группы.

### LogLevel

Уровень лога (типа `DEBUG` или `WARNING`).

### User

Сервис поддерживает аутентификацию, для этого нужны сущности пользователей. Пользователь может быть владельцем группы логов. Пользователь может писать логи в группу, которой владеет.
