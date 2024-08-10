from command import Command, CommandType, Direction

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
        pass
    
    def execute(self, command: Command):
        if command.command_type == CommandType.NULL:
            return
        
        if command.command_type == CommandType.PLACE:
            self._place(command.x, command.y, command.direction)
        
        if not self._placed:
            return
        
        if command.command_type == CommandType.MOVE:
            self._move()
        elif command.command_type == CommandType.LEFT:
            self._left()
        elif command.command_type == CommandType.RIGHT:
            self._right()
        elif command.command_type == CommandType.REPORT:
            self._report()