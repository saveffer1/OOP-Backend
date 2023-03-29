from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum
from src.model.util.mixin import DictMixin
### model
from src.model.account.account import Admin, User
import src

@dataclass
class System(DictMixin, ABC):
    account: AccountSystem

account = AccountSystem()

""" create admin account """
ADMIN = [
    Admin(0, "sff@mail.com", "sff", "123456"),
    Admin(0, "pai@mail.com", "pai", "123456"),
    Admin(0, "ton@mail.com", "jeak", "123456"),
    Admin(0, "nook@mail.com", "nook", "123456")
]
for admin in ADMIN:
    admin.id = account.admin_id
    account.admin_account[admin.email] = admin
    account.admin_id += 1

system = System(account)