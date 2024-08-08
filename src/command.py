from dataclasses import dataclass
from typing import Optional

@dataclass
class Command:
    command_type: str
    x: Optional[int] = None
    y: Optional[int] = None
    direction: Optional[str] = None