from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from src.model.account import UserStatus

class AccountSchema(BaseModel):
    email: EmailStr
    username: str
    password: str


class UpdateAccountModel(BaseModel):
    email: Optional[EmailStr]
    username: Optional[str]
    password: Optional[str]


class UserSchema(AccountSchema):
    status: UserStatus = UserStatus.online


class UpdateUserModel(UpdateAccountModel):
    status: Optional[UserStatus]
    