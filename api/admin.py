from hashlib import md5
from typing import Optional
from fastapi import FastAPI
from api.globals import settings, db

from loguru import logger
from sqladmin import Admin, ModelView

from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

import sqlalchemy as sa

from db import LogGroup, LogItem, LogLevel, User


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

    authentication_backend = AdminAuth(secret_key=_encode_token(settings.admin_email, settings.admin_password))

    admin = Admin(
        app,
        db.engine,
        authentication_backend=authentication_backend,
        title="KLogger Admin"
    )

    logger.info("REGISTER ALL DB TABLES IN ADMIN")


    class LogGroupAdmin(ModelView, model=LogGroup):
        icon = 'fa-solid fa-folder'
        column_list = [LogGroup.name, LogGroup.description, LogGroup.user, LogGroup.id]
        column_details_exclude_list = [LogGroup.log_items]
    admin.add_view(LogGroupAdmin)


    class LogLevelAdmin(ModelView, model=LogLevel):
        icon = 'fa-solid fa-tag'
        column_list = [LogLevel.name]
        column_details_exclude_list = [LogLevel.log_items]
        can_edit = False
        can_view_details = False
    admin.add_view(LogLevelAdmin)


    class LogItemAdmin(ModelView, model=LogItem):
        icon = 'fa-solid fa-layer-group'
        column_list = [LogItem.log_level, LogItem.message, LogItem.timestamp, LogItem.log_group, LogItem.id]
        column_sortable_list = [LogItem.timestamp]
        column_searchable_list = [LogItem.log_level, LogItem.message]
        column_default_sort = (LogItem.timestamp, True)
    admin.add_view(LogItemAdmin)


    class UserAdmin(ModelView, model=User):
        icon = 'fa-solid fa-user'
        can_edit = False
        can_create = False
        column_list = [User.email, User.id, User.created_at]
    admin.add_view(UserAdmin)


__all__ = [
    setup_admin
]
