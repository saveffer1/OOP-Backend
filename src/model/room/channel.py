from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime
from model.util.mixin import DictMixin

@dataclass
class Channel(DictMixin):
    id: int
    name: str
    type: str
    catagory: str
    _messages: Optional[list] = field(default_factory=list)

    def create_invite(self):
        pass
