
from loguru import logger
from pydantic import ValidationError

from controllers.log_item import LogItemController
from controllers.log_group import LogGroupController
from controllers.log_level import LogLevelController
from controllers.user import UserController

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

user_controller = UserController()
log_level_controller = LogLevelController()
log_group_controller = LogGroupController()
log_item_controller = LogItemController()

__all__ = [
    settings,
    db,
    user_controller,
    log_level_controller,
    log_group_controller,
    log_item_controller
]
