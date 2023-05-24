from fastapi import FastAPI
from api.globals import settings

from loguru import logger
from sqladmin import Admin, ModelView

import sqlalchemy as sa


def _create_sync_engine(user, password, host, port, name):
    logger.info("CREATE SYNC DB ENGINE FOR ADMIN")
    pg_dsn = f'postgresql://{user}:{password}@{host}:{port}/{name}'
    engine = sa.create_engine(
        pg_dsn,
        echo=settings.debug
    )
    return engine


def setup_admin(app: FastAPI):
    logger.info("SETUP ADMIN FOR APP")
    engine = _create_sync_engine(
        settings.db_user,
        settings.db_password,
        settings.db_host,
        settings.db_port,
        settings.db_name
    )
    admin = Admin(app, engine)

    logger.info("REGISTER ALL DB TABLES IN ADMIN")

    from db import LogGroup, LogItem, LogLevel, User


    class LogGroupAdmin(ModelView, model=LogGroup):
        column_list = [LogGroup.name, LogGroup.description, LogGroup.id]
    admin.add_view(LogGroupAdmin)


    class LogLevelAdmin(ModelView, model=LogLevel):
        column_list = [LogLevel.name]
    admin.add_view(LogLevelAdmin)


    class LogItemAdmin(ModelView, model=LogItem):
        column_list = [LogItem.log_level, LogItem.message, LogItem.timestamp, LogItem.log_group, LogItem.id]
    admin.add_view(LogItemAdmin)

    class UserAdmin(ModelView, model=User):
        column_list = [User.email, User.id, User.created_at]
    admin.add_view(UserAdmin)


__all__ = [
    setup_admin
]
