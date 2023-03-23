from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from src.account import UserStatus

class AccountSchema(BaseModel):
    email: EmailStr = Field(...)
    username: str = Field(...)
    password: str = Field(...)

class UpdateAccountModel(BaseModel):
    email: Optional[EmailStr]
    username: Optional[str]
    password: Optional[str]

class UserSchema(AccountSchema):
    status: UserStatus = UserStatus.online

class UpdateUserModel(BaseModel):
    email: Optional[EmailStr]
    username: Optional[str]
    password: Optional[str]
    status: Optional[UserStatus]
    
def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }

def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
