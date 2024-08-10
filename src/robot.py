from command import Command, CommandType, Direction
from output import Output, Report

class Robot:
    _min_x = 0
    _max_x = 4
    _min_y = 0
    _max_y = 4
    
    _direction_to_vectors = {
        Direction.NORTH : (0, 1),
        Direction.SOUTH : (0, -1),
        Direction.EAST : (1, 0),
        Direction.WEST : (-1, 0),
    }
    
    _vectors_to_direction = {v: d for d, v in _direction_to_vectors.items()}
    
    def __init__(self):
        self._position = None
        self._direction_vector = None
        self._placed = False
    
    def _is_within_bounds(self, x: int, y: int) -> bool:
        return self._min_x <= x <= self._max_x and self._min_y <= y <= self._max_y
        
    def _place(self, x: int, y: int, direction: Direction):
        if self._is_within_bounds(x, y):
            self._position = (x, y)
            self._direction_vector = self._direction_to_vectors[direction]
            self._placed = True
    
    def _move(self):
        dx, dy = self._direction_vector
        new_x = self._position[0] + dx 
        new_y = self._position[1] + dy
        if self._is_within_bounds(new_x, new_y):
            self._position = (new_x, new_y)
            
    def _left(self):
        pass
    
    def _right(self):
        pass
    
    def _report(self):
        return Report(self._position[0], self._position[1], self._vectors_to_direction[self._direction_vector])
    
    def execute(self, command: Command):
        if command.command_type == CommandType.NULL:
            return Output(CommandType.NULL)
        
        if command.command_type == CommandType.PLACE:
            self._place(command.x, command.y, command.direction)
            return Output(CommandType.PLACE)
        
        if not self._placed:
            return Output(CommandType.NULL)
        
        if command.command_type == CommandType.MOVE:
            self._move()
            return Output(CommandType.MOVE)
        if command.command_type == CommandType.LEFT:
            self._left()
            return Output(CommandType.LEFT)
        if command.command_type == CommandType.RIGHT:
            self._right()
            return Output(CommandType.RIGHT)
        if command.command_type == CommandType.REPORT:
            report = self._report()
            return Output(CommandType.REPORT, report)
        
        return Output(CommandType.NULL)