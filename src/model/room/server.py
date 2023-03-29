from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime
from src.model.util import DictMixin, EmailStr, UserStatus
from src.model.account import Admin, User

@dataclass
class Server(DictMixin):
    id:int
    name:str
    server_icon:Optional[str] = "https://res.cloudinary.com/dmtnecr2n/image/upload/UserAvatar/DiscordDefaultAvatar.jpg"
    owner_id:int
    roles:list 
    invites:list
    members:list
    channel_list:list

    def create_channel(self):
        pass

    def update_channel(self):
        pass

    def delete_channel(self):
        pass

    def create_role(self):
        pass

    def apply_role(self):
        pass

