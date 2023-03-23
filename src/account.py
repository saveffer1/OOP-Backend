from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional
from enum import Enum
from image import Image

class UserStatus(Enum):
    online = 1
    idel = 2
    dnd = 3
    invisible = 4
    
@dataclass
class Account(ABC):
    email: str
    user_name: str
    user_pass: str
    avatar: Optional[str] = "https://res.cloudinary.com/dmtnecr2n/image/upload/v1679560565/DiscordDefaultAvatar.jpg"
    
    @abstractmethod
    def login(self):
        pass
    
    @abstractmethod
    def logout(self):
        pass
    
    @abstractmethod
    def upload_avatar(self):
        pass
    
class Admin(Account):
    def login(self):
        print("Admin login")
    
    def logout(self):
        print("Admin logout")
    
    def upload_avatar(self):
        print("Admin upload avatar")
    
class User(Account):
    status : UserStatus = UserStatus.online
    
    def login(self):
        print("User login")
    
    def logout(self):
        print("User logout")
    
    def change_status(self, status: UserStatus):
        self.status = status
    
    def change_avatar(self, avatar: Image):
        self.avatar = avatar.upload_image()