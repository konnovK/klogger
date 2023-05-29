import datetime
from pydantic import BaseModel, UUID4, EmailStr

from api.schemas.log_group import LogGroupResponse


class CreateUserRequest(BaseModel):
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    access_token_expires_in: int


class UserResponse(BaseModel):
    id: UUID4
    created_at: datetime.datetime
    email: EmailStr

    log_groups: list[LogGroupResponse]

