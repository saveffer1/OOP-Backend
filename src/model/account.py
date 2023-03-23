from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum
from src.model.base.image import Image
from src.model.base.mixin import DictMixin

class UserStatus(Enum):
    online = 1
    idel = 2
    dnd = 3
    invisible = 4

@dataclass
class Account(DictMixin, ABC):
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

@dataclass
class AccountSystem(DictMixin):
    user_account: list = field(default_factory=list)
    admin_account: list = field(default_factory=list)

    def add_user(self, account: User):
        if account in self.user_account:
            return False
        elif account.email in [user.email for user in self.user_account]:
            return False
        else:
            self.user_account.append(account)
            return True
    
    def user_login(self, account: User):
        if account in self.user_account:
            account.login()
            return True
        else:
            return False