import datetime
from pydantic import BaseModel, UUID4

from controllers.schemas.log_level import LogLevelResponse
from controllers.schemas.log_group import LogGroupResponse


class LogItemResponse(BaseModel):
    id: UUID4
    created_at: datetime.datetime
    log_level: LogLevelResponse
    log_group: LogGroupResponse
    message: str
    timestamp: datetime.datetime

    class Config:
        orm_mode = True
