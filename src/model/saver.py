from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime


@dataclass
class Server:
    id:int
    name:str
    image:Optional[str] = "https://res.cloudinary.com/dmtnecr2n/image/upload/UserAvatar/DiscordDefaultAvatar.jpg"
    owner_id:int
    role:list 
    invites:list
    member:list
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
    
@dataclass
class Channel:
    id:int
    name:str
    type:str
    catagory:str
    _messages:Optional[list] = field(default_factory = list)

    def create_invite(self):
        pass


@dataclass
class Invite:
    id:int
    channel_list:list
    auther_id:int
    date_create:datetime


@dataclass
class Role:
    name:str
    color:str
    permissions:list
