from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum
import bcrypt
from src.model.util.mixin import DictMixin
from src.model.util.enumclass import UserStatus
from src.model.util.email import EmailStr
from src.model.account.account import Admin, User

@dataclass
class ServerSystem(DictMixin):
    pass
