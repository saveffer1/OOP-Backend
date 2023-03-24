from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum
from src.model.base.image import Image
from src.model.base.mixin import DictMixin
### model
from src.model.account import AccountSystem

@dataclass
class System(DictMixin, ABC):
    account: AccountSystem

account = AccountSystem()
system = System(account)
