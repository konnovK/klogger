import datetime
from pydantic import BaseModel


class CreateLogLevelRequest(BaseModel):
    name: str


class LogLevelResponse(BaseModel):
    name: str
    created_at: datetime.datetime
