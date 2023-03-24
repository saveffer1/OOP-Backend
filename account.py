from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum
from src.model.base.image import Image
from src.model.base.mixin import DictMixin
from src.model.base.enumclass import UserStatus
from src.schema.accountschema import (
    AccountSchema as AdminSchema, UpdateAccountModel as UpdateAdminModel,
    UserSchema, UpdateUserModel, LoginSchema
)

@dataclass
class Account(DictMixin, ABC):
    id: int
    email: str
    username: str
    password: str
    avatar: Optional[str] = "https://res.cloudinary.com/dmtnecr2n/image/upload/v1679560565/DiscordDefaultAvatar.jpg"
    tag: Optional[str] = "0000"
    
    @abstractmethod
    def login(self):
        pass
    
    @abstractmethod
    def logout(self):
        pass
    
    def change_avatar(self, avatar: Image):
        self.avatar = avatar.upload_image()
    
class Admin(Account):
    def login(self):
        print("Admin login")
    
    def logout(self):
        print("Admin logout")
    
class User(Account):
    status : UserStatus = UserStatus.online
    
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
            account = User(self.id, schema.email, schema.username, schema.password)
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
            if schema.password == self.user_account[schema.email].password:
                self.user_account[schema.email].login()
                return True
            else:
                return False
        else:
            return False


system = AccountSystem()
y = UserSchema(email="sf@user.gg", username="sf10s", password="save2345")


def login(user: LoginSchema):
    if system.user_login(user):
        return {'status_code': 200, 'detail': 'success', 'data': system.user_login(user)}
    else:
        return {'status_code': 401, 'detail': 'error', 'data': system.user_login(user)}
    

system.add_user(y)
print(login(y))
