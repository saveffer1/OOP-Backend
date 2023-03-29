from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime
from model.util.mixin import DictMixin

@dataclass
class Invite(DictMixin):
    id:int
    channel_list:list
    auther_id:int
    date_create:datetime