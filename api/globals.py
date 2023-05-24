
from typing import Literal
from loguru import logger
from pydantic import ValidationError
from db import DB
from api.settings import APISettings


try:
    settings = APISettings()
    if settings.debug:
        logger.warning("DEBUG MODE IS True")
except ValidationError as err:
    logger.critical(err)
    exit(1)

db = DB(
    settings.db_user,
    settings.db_password,
    settings.db_host,
    settings.db_port,
    settings.db_name,
    settings.debug,
)


log_levels = Literal['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']


__all__ = [
    settings,
    db,
    log_levels
]
