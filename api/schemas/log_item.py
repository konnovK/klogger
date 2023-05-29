import datetime
from pydantic import BaseModel, UUID4

from api.schemas.log_level import LogLevelResponse
from api.schemas.log_group import LogGroupResponse


class CreateLogItemRequest(BaseModel):
    level: str
    message: str
    timestamp: datetime.datetime


class LogItemResponse(BaseModel):
    id: UUID4
    created_at: datetime.datetime
    log_level: LogLevelResponse
    log_group: LogGroupResponse
    message: str
    timestamp: datetime.datetime


class ListLogItemResponse(BaseModel):
    count: int
    items: list[LogItemResponse]
