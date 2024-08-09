import re
from command import Command, CommandType, Direction

class CommandParser:
    VALID_COMMAND_TYPES = {"PLACE", "MOVE", "LEFT", "RIGHT", "REPORT"}
    
    def parse(self, command_str: str) -> Command:
        # Note: Assuming a strict format for commands, stops program on invalid format
        command_str = command_str.strip()
        command_parts = command_str.split()
        
        # If empty command, return NULL command to skip action
        if len(command_parts) == 0:
            return Command(CommandType.NULL)
        
        if len(command_parts) > 2:
            raise ValueError(f"Invalid command format, too many parts: {command_str}")
        
        if command_parts[0] not in self.VALID_COMMAND_TYPES:
            raise ValueError(f"Invalid command type: {command_parts[0]}")
        
        if command_parts[0] == "PLACE":
            pattern = r"^(\d+),(\d+),(NORTH|SOUTH|EAST|WEST)$"
            match = re.match(pattern, command_parts[1])
            if not match:
                raise ValueError(f"Invalid PLACE arguments: {command_parts[1]}")
            x_str, y_str, direction_str = match.groups()
            
            if direction_str == "NORTH":
                direction = Direction.NORTH
            elif direction_str == "SOUTH":
                direction = Direction.SOUTH
            elif direction_str == "EAST":
                direction = Direction.EAST
            elif direction_str == "WEST":
                direction = Direction.WEST
            else:
                raise ValueError(f"Invalid direction: {direction_str}")
            
            return Command(CommandType.PLACE, int(x_str), int(y_str), direction)
                            
        # Check for rest of Commands with no Arguments
        if len(command_parts) != 1:
            raise ValueError(f"Invalid command format, expecting no arguments for {command_parts[0]}: {command_str}")
        
        if command_parts[0] == "MOVE":
            return Command(CommandType.MOVE)
        
        if command_parts[0] == "LEFT":
            return Command(CommandType.LEFT)
        
        if command_parts[0] == "RIGHT":
            return Command(CommandType.RIGHT)
        
        if command_parts[0] == "REPORT":
            return Command(CommandType.REPORT)   