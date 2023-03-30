from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum
import bcrypt
from src.model.util import DictMixin, UserStatus, EmailStr
from src.model.account import Admin, User
from src.schema import AdminSchema, UserSchema, LoginSchema


@dataclass
class AccountSystem(DictMixin):
    user_account: dict = field(default_factory=dict)
    admin_account: dict = field(default_factory=dict)
    user_id: int = 1
    admin_id: int = 1

    def get_user_account(self):
        return [user for user in self.user_account.values()]
    
    def get_admin_account(self):
        return [admin for admin in self.admin_account.values()]
    
    def add_user(self, schema: UserSchema):
        """ register function add the user obj to user_account """
        if not self.user_account or schema.email not in self.user_account:
            hashed_password = bcrypt.hashpw(schema.password.encode('utf-8'), bcrypt.gensalt(5))
            if schema.username in [user.username for user in self.user_account.values()]:
                tag = max([int(user.tag) for user in self.user_account.values()]) + 1
                tag = str(tag).zfill(4)
                account = User(self.user_id, schema.email, schema.username, hashed_password, schema.avatar, tag=tag)
            else:
                account = User(self.user_id, schema.email, schema.username, hashed_password, schema.avatar)
            self.user_account[schema.email] = account
            self.user_id += 1
            return True
        else:
            return False
    
    def add_admin(self, schema: AdminSchema):
        """ add admin to admin_account """
        if not self.admin_account or schema.email not in self.admin_account:
            account = Admin(self.admin_id, schema.email, schema.username, schema.password.encode('utf-8'))
            self.admin_account[schema.email] = account
            self.admin_id += 1
            return True
        else:
            return False

    def check_password(self, input_password, check_password):
        """ function check the password """
        return bcrypt.checkpw(input_password.encode('utf-8'), check_password)
        
    def user_login(self, schema: LoginSchema):
        """ login function check email and password in user_account """
        if not self.user_account:
            return False
        elif schema.email in self.user_account:
            is_login_pass = self.check_password(
                schema.password, self.user_account[schema.email].password
            )
            login_state = is_login_pass
            if is_login_pass:
                self.user_account[schema.email].login()
            return login_state
        else:
            return False
    
    def admin_login(self, schema: LoginSchema):
        """ login function check email and password in admin_account """
        if not self.admin_account:
            return False
        elif schema.email in self.admin_account:
            is_login_pass = self.check_password(
                schema.password, self.admin_account[schema.email].password
            )
            login_state = is_login_pass
            if is_login_pass:
                self.admin_account[schema.email].login()
            return login_state
        else:
            return False
    
    def get_status(self, email: EmailStr):
        """ get user status """
        return self.user_account[email].status
    
    def set_status(self, email: EmailStr, status: UserStatus):
        """ set user status """
        self.user_account[email].status = status
    
    def get_avatar(self, email: EmailStr):
        """ get user avatar """
        return self.user_account[email].avatar
    
    def set_avatar(self, email: EmailStr, avatar: str):
        """ set user avatar """
        self.user_account[email].avatar = avatar