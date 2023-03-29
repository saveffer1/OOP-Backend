from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum
from src.model.util import DictMixin, UserStatus, EmailStr
@dataclass
class Account(DictMixin, ABC):
    id: int
    email: EmailStr
    username: str
    password: bytes
    avatar: Optional[str] = "https://res.cloudinary.com/dmtnecr2n/image/upload/UserAvatar/DiscordDefaultAvatar.jpg"
    tag: Optional[str] = "0000"
    
    @abstractmethod
    def login(self):
        pass
    
    @abstractmethod
    def logout(self):
        pass
    
    # def change_avatar(self, avatar: Image):
    #     self.avatar = avatar.upload_image()
    
class Admin(Account):
    def login(self):
        print("Admin login")
    
    def logout(self):
        print("Admin logout")
    
class User(Account):
    status : Optional[UserStatus] = UserStatus.online
    friends: Optional[list] = field(default_factory=list)
    notifications: Optional[list] = field(default_factory=list)
    
    def login(self):
        print("User login")
    
    def logout(self):
        print("User logout")
    
    def change_status(self, status: UserStatus):
        self.status = status
