from dataclasses import dataclass, field
from src.model.util import DictMixin, EmailStr, UserStatus
from src.model.account import Admin, User
@dataclass
class Role(DictMixin):
    name:str
    color:str
    permissions:list