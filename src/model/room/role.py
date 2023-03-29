from dataclasses import dataclass, field
from src.model.util.mixin import DictMixin
@dataclass
class Role(DictMixin):
    name:str
    color:str
    permissions:list