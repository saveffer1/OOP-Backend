from typing import Optional
from pydantic import BaseModel, Field
from src.model.base.enumclass import UserStatus

class AccountSchema(BaseModel):
    email: str
    username: str
    password: str

class UpdateAccountModel(BaseModel):
    email: Optional[str]
    username: Optional[str]
    password: Optional[str]

class LoginSchema(BaseModel):
    email: str
    password: str
    
class UserSchema(AccountSchema):
    status: UserStatus = UserStatus.online

class UpdateUserModel(UpdateAccountModel):
    status: Optional[UserStatus] = UserStatus.online
    