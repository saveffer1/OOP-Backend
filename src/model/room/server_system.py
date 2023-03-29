from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum
from src.model.util import DictMixin, EmailStr, UserStatus

@dataclass
class ServerSystem(DictMixin):
    pass
