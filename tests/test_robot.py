import pytest
from unittest.mock import patch
from dataclasses import asdict

from src.robot import Robot
from src.command import Command, CommandType, Direction
from src.output import Output, Report

@pytest.fixture
def robot():
    return Robot()

class TestRobot:
    def test_robot_initialized_with_place_set_to_false(self):
        robot = Robot()
        assert robot._placed == False
        
    def test_report_function_not_called_when_not_placed(self, robot):
        assert robot._placed == False
        with patch.object(robot, '_report') as mock_report:
            output = robot.execute(Command(CommandType.REPORT))
            assert asdict(output) == asdict(Output(CommandType.NULL))
            mock_report.assert_not_called()
            
    @pytest.mark.parametrize("place_command", [
        Command(CommandType.PLACE, 0, 0, Direction.NORTH),
        Command(CommandType.PLACE, 1, 2, Direction.SOUTH),
        Command(CommandType.PLACE, 3, 4, Direction.EAST),
        Command(CommandType.PLACE, 4, 4, Direction.WEST),
    ])
    def test_report_returns_correct_output_when_placed(self, robot, place_command):
        robot.execute(place_command)
        assert robot._placed == True
        output = robot.execute(Command(CommandType.REPORT))
        expected_output = Output(CommandType.REPORT, Report(place_command.x, place_command.y, place_command.direction))
        assert asdict(output) == asdict(expected_output)
            
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
        output = robot.execute(Command(CommandType.REPORT))
        expected_output = Output(CommandType.REPORT, Report(place_command.x, place_command.y, place_command.direction))
        assert asdict(output) == asdict(expected_output)
        
    @pytest.mark.parametrize("place_command", [
        Command(CommandType.PLACE, 0, 0, Direction.NORTH),
        Command(CommandType.PLACE, 0, 4, Direction.SOUTH),
        Command(CommandType.PLACE, 4, 0, Direction.EAST),
        Command(CommandType.PLACE, 2, 3, Direction.WEST),
    ])
    def test_place_with_valid_coordinates_sets_correct_values_even_when_already_placed(self, robot, place_command):
        robot.execute(Command(CommandType.PLACE, 0, 0, Direction.NORTH))
        assert robot._placed == True
        robot.execute(place_command)
        assert robot._placed == True
        output = robot.execute(Command(CommandType.REPORT))
        expected_output = Output(CommandType.REPORT, Report(place_command.x, place_command.y, place_command.direction))
        assert asdict(output) == asdict(expected_output)
        
    def test_move_function_not_called_when_not_placed(self, robot):
        assert robot._placed == False
        with patch.object(robot, '_move') as mock_move:
            output = robot.execute(Command(CommandType.MOVE))
            assert asdict(output) == asdict(Output(CommandType.NULL))
            mock_move.assert_not_called()
    
    @pytest.mark.parametrize("place_command", [
        Command(CommandType.PLACE, 0, 4, Direction.NORTH),
        Command(CommandType.PLACE, 0, 0, Direction.SOUTH),
        Command(CommandType.PLACE, 4, 0, Direction.EAST),
        Command(CommandType.PLACE, 0, 0, Direction.WEST),
    ])
    def test_move_does_not_change_coordinates_when_moving_out_of_bounds(self, robot, place_command):
        robot.execute(place_command)
        robot.execute(Command(CommandType.MOVE))
        output = robot.execute(Command(CommandType.REPORT))
        expected_output = Output(CommandType.REPORT, Report(place_command.x, place_command.y, place_command.direction))
        assert asdict(output) == asdict(expected_output)
    
    @pytest.mark.parametrize("place_command, expected_coordinates", [
        (Command(CommandType.PLACE, 2, 2, Direction.NORTH), (2, 3)),
        (Command(CommandType.PLACE, 2, 2, Direction.SOUTH), (2, 1)),
        (Command(CommandType.PLACE, 2, 2, Direction.EAST), (3, 2)),
        (Command(CommandType.PLACE, 2, 2, Direction.WEST), (1, 2)),
    ])    
    def test_move_changes_coordinates_by_one_when_moving_within_bounds(self, robot, place_command, expected_coordinates):        
        robot.execute(place_command)
        robot.execute(Command(CommandType.MOVE))
        output = robot.execute(Command(CommandType.REPORT))
        expected_output = Output(CommandType.REPORT, Report(expected_coordinates[0], expected_coordinates[1], place_command.direction))
        assert asdict(output) == asdict(expected_output)
        
    def test_left_function_not_called_when_not_placed(self, robot):
        assert robot._placed == False
        with patch.object(robot, '_left') as mock_left:
            output = robot.execute(Command(CommandType.LEFT))
            assert asdict(output) == asdict(Output(CommandType.NULL))
            mock_left.assert_not_called()

    @pytest.mark.parametrize("initial_direction, expected_direction", [
        (Direction.NORTH, Direction.WEST),
        (Direction.WEST, Direction.SOUTH),
        (Direction.SOUTH, Direction.EAST),
        (Direction.EAST, Direction.NORTH),
    ])          
    def test_left_updates_direction_correctly(self, robot, initial_direction, expected_direction):
        robot.execute(Command(CommandType.PLACE, 0, 0, initial_direction)),
        robot.execute(Command(CommandType.LEFT))
        output = robot.execute(Command(CommandType.REPORT))
        expected_output = Output(CommandType.REPORT, Report(0, 0, expected_direction))
        assert asdict(output) == asdict(expected_output)

    def test_right_function_not_called_when_not_placed(self, robot):
        assert robot._placed == False
        with patch.object(robot, '_right') as mock_right:
            output = robot.execute(Command(CommandType.RIGHT))
            assert asdict(output) == asdict(Output(CommandType.NULL))
            mock_right.assert_not_called()
            
    @pytest.mark.parametrize("initial_direction, expected_direction", [
        (Direction.NORTH, Direction.EAST),
        (Direction.EAST, Direction.SOUTH),
        (Direction.SOUTH, Direction.WEST),
        (Direction.WEST, Direction.NORTH),
    ])          
    def test_right_updates_direction_correctly(self, robot, initial_direction, expected_direction):
        robot.execute(Command(CommandType.PLACE, 0, 0, initial_direction)),
        robot.execute(Command(CommandType.RIGHT))
        output = robot.execute(Command(CommandType.REPORT))
        expected_output = Output(CommandType.REPORT, Report(0, 0, expected_direction))
        assert asdict(output) == asdict(expected_output)