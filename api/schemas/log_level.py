import datetime
from pydantic import BaseModel

from api.globals import log_levels


class CreateLogLevelRequest(BaseModel):
    name: log_levels


class LogLevelResponse(BaseModel):
    name: str
    created_at: datetime.datetime

    class Config:
        orm_mode = True

