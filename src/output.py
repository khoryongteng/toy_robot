from command import CommandType, Direction
from dataclasses import dataclass
from typing import Optional

@dataclass
class Report():
    x: int
    y: int
    direction: Direction

@dataclass
class Output():
    command_ran: Optional[CommandType] = None
    report: Optional[Report] = None