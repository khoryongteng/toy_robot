import pytest
from unittest.mock import patch
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
    
    @pytest.mark.parametrize("place_command, expected_position, expected_direction_vector", [
        (Command(CommandType.PLACE, 0, 0, Direction.NORTH), (0, 0), (0, 1)),
        (Command(CommandType.PLACE, 0, 4, Direction.SOUTH), (0, 4), (0, -1)),
        (Command(CommandType.PLACE, 4, 0, Direction.EAST), (4, 0), (1, 0)),
        (Command(CommandType.PLACE, 2, 3, Direction.WEST), (2, 3), (-1, 0)),
    ])       
    def test_place_with_valid_coordinates_sets_correct_values(self, robot, place_command, expected_position, expected_direction_vector):
        robot.execute(place_command)
        assert robot._placed == True
        assert robot._position == expected_position
        assert robot._direction_vector == expected_direction_vector
        
    @pytest.mark.parametrize("place_command, expected_position, expected_direction_vector", [
        (Command(CommandType.PLACE, 0, 0, Direction.NORTH), (0, 0), (0, 1)),
        (Command(CommandType.PLACE, 0, 4, Direction.SOUTH), (0, 4), (0, -1)),
        (Command(CommandType.PLACE, 4, 0, Direction.EAST), (4, 0), (1, 0)),
        (Command(CommandType.PLACE, 2, 3, Direction.WEST), (2, 3), (-1, 0)),
    ])
    def test_place_with_valid_coordinates_sets_correct_values_even_when_already_placed(self, robot, place_command, expected_position, expected_direction_vector):
        robot.execute(Command(CommandType.PLACE, 0, 0, Direction.NORTH))
        robot.execute(place_command)
        assert robot._placed == True
        assert robot._position == expected_position
        assert robot._direction_vector == expected_direction_vector
        
    def test_move_function_not_called_when_not_placed(self, robot):
        assert robot._placed == False
        with patch.object(robot, '_move') as mock_move:
            robot.execute(Command(CommandType.MOVE))
            mock_move.assert_not_called()
            
    def test_move_function_called_when_placed(self, robot):
        robot.execute(Command(CommandType.PLACE, 0, 0, Direction.NORTH))
        assert robot._placed == True
        with patch.object(robot, '_move') as mock_move:
            robot.execute(Command(CommandType.MOVE))
            mock_move.assert_called_once()
    
    @pytest.mark.parametrize("place_command", [
        Command(CommandType.PLACE, 0, 4, Direction.NORTH),
        Command(CommandType.PLACE, 0, 0, Direction.SOUTH),
        Command(CommandType.PLACE, 4, 0, Direction.EAST),
        Command(CommandType.PLACE, 0, 0, Direction.WEST),
    ])
    def test_move_does_not_change_coordinates_when_moving_out_of_bounds(self, robot, place_command):
        robot.execute(place_command)
        robot.execute(Command(CommandType.MOVE))
        assert robot._position == (place_command.x, place_command.y)
    
    @pytest.mark.parametrize("place_command, expected_coordinates", [
        (Command(CommandType.PLACE, 2, 2, Direction.NORTH), (2, 3)),
        (Command(CommandType.PLACE, 2, 2, Direction.SOUTH), (2, 1)),
        (Command(CommandType.PLACE, 2, 2, Direction.EAST), (3, 2)),
        (Command(CommandType.PLACE, 2, 2, Direction.WEST), (1, 2)),
    ])    
    def test_move_changes_coordinates_by_one_when_moving_within_bounds(self, robot, place_command, expected_coordinates):
        robot.execute(place_command)
        robot.execute(Command(CommandType.MOVE))
        assert robot._position == expected_coordinates