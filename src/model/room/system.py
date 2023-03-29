from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum
import bcrypt
from src.model.util import DictMixin, EmailStr, UserStatus
from src.model.account import Admin, User

@dataclass
class ServerSystem(DictMixin):
    pass
