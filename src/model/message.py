from dataclasses import dataclass,field
from typing import Optional
from datetime import datetime


@dataclass
class Message:
    id:int
    sender:str
    content:str
    channel_id:int
    timestamp:datetime
    edited_timestamp:datetime
    edited:bool
    pin:bool

    def send_emoji(self):
        pass

    def react_emoji(self):
        pass


    def send_message(self):
        pass
    
    def reply_message(self):
        pass

    def recive_message(self):
        pass
    





class Embedded:
    title:str
    description:str
    url:str
    color:str

class Attachment:
    filename:str
    file_type:str
    url:str


class Emoji:
    name:str
    # unicode_code: