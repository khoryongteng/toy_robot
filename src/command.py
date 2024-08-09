from dataclasses import dataclass
from enum import IntEnum
from typing import Optional

class CommandType(IntEnum):
    NULL = 0
    PLACE = 1 
    MOVE = 2 
    LEFT = 3 
    RIGHT = 4 
    REPORT = 5
    
class Direction(IntEnum):
    NORTH = 0
    SOUTH = 1
    EAST = 2
    WEST = 3
    
@dataclass
class Command:
    command_type: CommandType
    x: Optional[int] = None
    y: Optional[int] = None
    direction: Optional[Direction] = None