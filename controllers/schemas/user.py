import datetime
from pydantic import BaseModel, UUID4, EmailStr

from controllers.schemas.log_group import LogGroupResponse


class UserResponse(BaseModel):
    id: UUID4
    created_at: datetime.datetime
    email: EmailStr

    log_groups: list[LogGroupResponse]

    class Config:
        orm_mode = True
