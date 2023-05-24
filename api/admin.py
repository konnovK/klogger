from hashlib import md5
from typing import Optional
from fastapi import FastAPI
from api.globals import settings

from loguru import logger
from sqladmin import Admin, ModelView

from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

import sqlalchemy as sa

from db import LogGroup, LogItem, LogLevel, User


def _create_sync_engine(user, password, host, port, name):
    logger.info("CREATE SYNC DB ENGINE FOR ADMIN")
    pg_dsn = f'postgresql://{user}:{password}@{host}:{port}/{name}'
    engine = sa.create_engine(
        pg_dsn,
        echo=settings.debug
    )
    return engine


def _encode_token(email: str, password: str):
    return md5(f'{email}:{password}'.encode()).hexdigest()


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        # Validate username/password credentials
        # And update session
        if username == settings.admin_email and password == settings.admin_password:
            token = _encode_token(username, password)
            request.session.update({"token": token})
            return True
        return False
        

    async def logout(self, request: Request) -> bool:
        # Usually you'd want to just clear the session
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> Optional[RedirectResponse]:
        token = request.session.get("token")

        if token != _encode_token(settings.admin_email, settings.admin_password):
            return RedirectResponse(request.url_for("admin:login"), status_code=302)


def setup_admin(app: FastAPI):
    logger.info("SETUP ADMIN FOR APP")
    engine = _create_sync_engine(
        settings.db_user,
        settings.db_password,
        settings.db_host,
        settings.db_port,
        settings.db_name
    )

    authentication_backend = AdminAuth(secret_key=_encode_token(settings.admin_email, settings.admin_password))

    admin = Admin(app, engine, authentication_backend=authentication_backend)

    logger.info("REGISTER ALL DB TABLES IN ADMIN")


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
