
from loguru import logger
from pydantic import ValidationError
from db.db import DB
from api.settings import APISettings


try:
    settings = APISettings()
except ValidationError as err:
    logger.error(err)
    exit(1)

db = DB(
    settings.db_user,
    settings.db_password,
    settings.db_host,
    settings.db_port,
    settings.db_name,
    settings.debug,
)


__all__ = [
    settings,
    db,
]
