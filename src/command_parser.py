import re
from command import Command, CommandType, Direction

class CommandParser:
    _command_type_map = {
        "PLACE" : CommandType.PLACE,
        "MOVE" : CommandType.MOVE,
        "LEFT" : CommandType.LEFT,
        "RIGHT" : CommandType.RIGHT,
        "REPORT" : CommandType.REPORT,
    }
    
    _direction_map = {
        "NORTH" : Direction.NORTH,
        "SOUTH" : Direction.SOUTH,
        "EAST" : Direction.EAST,
        "WEST" : Direction.WEST,
    }
    
    def _parse_place_arguments(self, args_str: str) -> tuple[int, int, Direction]:
        pattern = r"^(\d+),(\d+),(NORTH|SOUTH|EAST|WEST)$"
        match = re.match(pattern, args_str)
        if not match:
            raise ValueError(f"Invalid PLACE arguments: {args_str}")
        x_str, y_str, direction_str = match.groups()
        return int(x_str), int(y_str), self._direction_map[direction_str]
    
    # Note: Assuming a strict format for commands, stops program on invalid format
    def parse(self, command_str: str) -> Command:
        command_str = command_str.strip()
        
        # If empty command, return NULL command to skip action
        if not command_str:
            return Command(CommandType.NULL)
        
        command_parts = command_str.split()
        if command_parts[0] not in self._command_type_map:
            raise ValueError(f"Invalid command type: {command_parts[0]}")
        
        command_type = self._command_type_map[command_parts[0]]
        if command_type == CommandType.PLACE:
            if len(command_parts) != 2:
                raise ValueError(f"Invalid command format, no arguments provided for PLACE command: {command_str}  Example: PLACE 1,2,NORTH")
            x, y, direction = self._parse_place_arguments(command_parts[1])
            return Command(CommandType.PLACE, x, y, direction)
                            
        # Check for rest of Commands with no Arguments
        if len(command_parts) != 1:
            raise ValueError(f"Invalid command format, expecting no arguments for {command_parts[0]}: {command_str}")
        
        return Command(command_type)