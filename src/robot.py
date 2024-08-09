from command import Command, CommandType, Direction

class Robot:
    def __init__(self):
        self.coordinates = None
        self.direction = None
        self.placed = False
        
    def execute(self, command: Command):
        pass