import datetime
from pydantic import BaseModel, UUID4


class LogGroupResponse(BaseModel):
    id: UUID4
    created_at: datetime.datetime

    name: str
    description: str

    class Config:
        orm_mode = True
