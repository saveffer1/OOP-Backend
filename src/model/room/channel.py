from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime
from src.model.util import DictMixin, EmailStr, UserStatus

@dataclass
class Channel(DictMixin):
    id: int
    name: str
    type: str
    catagory: str
    _messages: Optional[list] = field(default_factory=list)

    def create_invite(self):
        pass
