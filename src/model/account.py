from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum
import bcrypt
from src.model.base.mixin import DictMixin
from src.model.base.enumclass import UserStatus
from src.model.base.email import EmailStr
from src.schema.accountschema import (
    AccountSchema as AdminSchema, UpdateAccountModel as UpdateAdminModel,
    UserSchema, UpdateUserModel, LoginSchema
)

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

@dataclass
class AccountSystem(DictMixin):
    user_account: dict = field(default_factory=dict)
    admin_account: dict = field(default_factory=dict)
    id: int = 1

    def add_user(self, schema: UserSchema):
        """ register function add the user obj to user_account """
        if not self.user_account or schema.email not in self.user_account:
            if schema.username in [user.username for user in self.user_account.values()]:
                tag = max([int(user.tag) for user in self.user_account.values()]) + 1
                tag = str(tag).zfill(4)
                account = User(self.id, schema.email, schema.username, schema.password, schema.avatar, tag=tag)
            else:
                account = User(self.id, schema.email, schema.username, schema.password, schema.avatar)
            self.user_account[schema.email] = account
            self.id += 1
            return True
        else:
            return False
    
    def user_login(self, schema: LoginSchema):
        """ login function check email and password in user_account """
        if not self.user_account:
            return False
        elif schema.email in self.user_account:
            if bcrypt.checkpw(schema.password.encode('utf-8'), self.user_account[schema.email].password):
                self.user_account[schema.email].login()
                return True
            else:
                return False
        else:
            return False
