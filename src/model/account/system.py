from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum
import bcrypt
from src.model.util.mixin import DictMixin
from src.model.util.enumclass import UserStatus
from src.model.util.email import EmailStr
from src.model.account.account import Admin, User
from src.schema.accountschema import (
    AccountSchema as AdminSchema, UpdateAccountModel as UpdateAdminModel,
    UserSchema, UpdateUserModel, LoginSchema
)


@dataclass
class AccountSystem(DictMixin):
    user_account: dict = field(default_factory=dict)
    admin_account: dict = field(default_factory=dict)
    user_id: int = 1
    admin_id: int = 1

    def add_user(self, schema: UserSchema):
        """ register function add the user obj to user_account """
        if not self.user_account or schema.email not in self.user_account:
            if schema.username in [user.username for user in self.user_account.values()]:
                tag = max([int(user.tag)
                          for user in self.user_account.values()]) + 1
                tag = str(tag).zfill(4)
                account = User(self.user_id, schema.email, schema.username,
                               schema.password, schema.avatar, tag=tag)
            else:
                account = User(self.user_id, schema.email,
                               schema.username, schema.password, schema.avatar)
            self.user_account[schema.email] = account
            self.user_id += 1
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
