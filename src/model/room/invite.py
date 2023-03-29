from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime
from src.model.util import DictMixin, EmailStr, UserStatus
@dataclass
class Invite(DictMixin):
    id:int
    channel_list:list
    auther_id:int
    date_create:datetime