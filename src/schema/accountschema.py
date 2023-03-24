from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from src.model.base.enumclass import UserStatus

class AccountSchema(BaseModel):
    email: EmailStr
    username: str
    password: str

class UpdateAccountModel(BaseModel):
    email: Optional[EmailStr]
    username: Optional[str]
    password: Optional[str]

class LoginSchema(BaseModel):
    email: EmailStr
    password: str
    
class UserSchema(AccountSchema):
    status: UserStatus = UserStatus.online

class UpdateUserModel(UpdateAccountModel):
    status: Optional[UserStatus] = UserStatus.online
    