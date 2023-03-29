from typing import Optional
from pydantic import BaseModel, Field
from src.model.util.enumclass import UserStatus
from src.model.util.email import EmailStr

class AccountSchema(BaseModel):
    email: EmailStr
    username: str
    password: bytes
    avatar: Optional[str] = "https://res.cloudinary.com/dmtnecr2n/image/upload/UserAvatar/DiscordDefaultAvatar.jpg"

class UpdateAccountModel(BaseModel):
    email: Optional[EmailStr]
    username: Optional[str]
    password: Optional[str]
    avatar: Optional[str]

class LoginSchema(BaseModel):
    email: EmailStr
    password: str
    
class UserSchema(AccountSchema):
    status: UserStatus = UserStatus.online

class UpdateUserModel(UpdateAccountModel):
    status: Optional[UserStatus] = UserStatus.online
    