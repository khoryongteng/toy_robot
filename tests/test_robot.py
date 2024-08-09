import pytest
from src.robot import Robot
from src.command import Command, CommandType, Direction

@pytest.fixture
def robot():
    return Robot()
 
class TestRobot:
    def test_robot_initialized_with_place_set_to_false(self):
        robot = Robot()
        assert robot._placed == False
            
    @pytest.mark.parametrize("place_command", [
        Command(CommandType.PLACE, -1, 0, Direction.NORTH),
        Command(CommandType.PLACE, 5, 0, Direction.SOUTH),
        Command(CommandType.PLACE, 0, -1, Direction.EAST),
        Command(CommandType.PLACE, 0, 5, Direction.WEST),
    ])   
    def test_place_invalid_coordinates_does_nothing(self, robot, place_command):
        state_before = robot.__dict__.copy()
        robot.execute(place_command)
        state_after = robot.__dict__.copy()
        assert state_before == state_after
    
    @pytest.mark.parametrize("place_command", [
        Command(CommandType.PLACE, 0, 0, Direction.NORTH),
        Command(CommandType.PLACE, 0, 4, Direction.SOUTH),
        Command(CommandType.PLACE, 4, 0, Direction.EAST),
        Command(CommandType.PLACE, 2, 3, Direction.WEST),
    ])       
    def test_place_with_valid_coordinates_sets_correct_values(self, robot, place_command):
        robot.execute(place_command)
        assert robot._placed == True
        assert robot._x == place_command.x
        assert robot._y == place_command.y
        assert robot._direction == place_command.direction
        
    @pytest.mark.parametrize("place_command", [
        Command(CommandType.PLACE, 0, 0, Direction.NORTH),
        Command(CommandType.PLACE, 0, 4, Direction.SOUTH),
        Command(CommandType.PLACE, 4, 0, Direction.EAST),
        Command(CommandType.PLACE, 2, 3, Direction.WEST),
    ])       
    def test_place_with_valid_coordinates_sets_correct_values_even_when_already_placed(self, robot, place_command):
        robot.execute(Command(CommandType.PLACE, 0, 0, Direction.NORTH))
        robot.execute(place_command)
        assert robot._placed == True
        assert robot._x == place_command.x
        assert robot._y == place_command.y
        assert robot._direction == place_command.direction