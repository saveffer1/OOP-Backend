from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum
### model
from src.model.util import DictMixin, EmailStr, UserStatus
from src.model.account import AccountSystem, Admin
from src.model.room import ServerSystem

@dataclass
class System(DictMixin, ABC):
    account: AccountSystem
    server: ServerSystem

account = AccountSystem()
server = ServerSystem()

system = System(account, server)
