# klogger

Простой сервис для сбора логов с системой пользователей, группами логов и т.д. Просто подключи к своей базе данных и работай.

## LogGroup

Логи группируются по группам. У группы есть владелец. Писать логи в группу может только владелец. Владелец группы - это тот пользователь, кто эту группу создал.

## LogItem

Сообщение логгера. Имеет группу, которой пренадлежит. Писать логи в группу может только владелец группы.

## LogLevel

Уровень лога (типа `DEBUG` или `WARNING`).

## User

Сервис поддерживает аутентификацию, для этого нужны сущности пользователей. Пользователь может быть владельцем группы логов. Пользователь может писать логи в группу, которой владеет.
