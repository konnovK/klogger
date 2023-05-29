import datetime
from pydantic import BaseModel


class LogLevelResponse(BaseModel):
    name: str
    created_at: datetime.datetime

    class Config:
        orm_mode = True
