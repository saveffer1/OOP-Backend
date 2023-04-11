from dataclasses import dataclass, field
from src.model.util import DictMixin, EmailStr, UserStatus

@dataclass
class Role(DictMixin):
    id: int
    name:str
    color:str
    permissions:list