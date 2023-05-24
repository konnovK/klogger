from api.globals import db
from db import DB


def get_db() -> DB:
    yield db
