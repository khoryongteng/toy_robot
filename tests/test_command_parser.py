import pytest
from src.command_parser import CommandParser
from src.command import Command, CommandType, Direction
from dataclasses import asdict

@pytest.fixture
def parser():
    return CommandParser()
 
class TestCommandParser:
    def test_parse_empty_command_returns_null_command(self, parser):
        command_str = ""
        expected = Command(CommandType.NULL)
        result = parser.parse(command_str)
        assert asdict(result) == asdict(expected)
        
    def test_parse_command_with_more_than_two_parts_raises_value_error(self, parser):
        command_str = "PLACE 1,2,NORTH MOVE MOVE"
        with pytest.raises(ValueError):
            parser.parse(command_str)
    
    @pytest.mark.parametrize("command_str", [
        "INVALID 1,2,NORTH",
        "MOVEE",
        "RRIGHT XXX",
        "TEST LEFT",
    ])
    def test_parse_invalid_command_type_raises_value_error(self, parser, command_str):
        with pytest.raises(ValueError):
            parser.parse(command_str)
            
    @pytest.mark.parametrize("command_str", [
        ("MOVE 1,2,NORTH"),
        ("LEFT XXX"),
        ("RIGHT 3,4,EAST"),
        ("REPORT ABCDE"),
    ])
    def test_parse_one_part_command_with_arguments_raises_value_error(self, parser, command_str):
        with pytest.raises(ValueError):
            parser.parse(command_str)
            
    @pytest.mark.parametrize("command_str, expected", [
        ("MOVE", Command(CommandType.MOVE)),
        ("LEFT", Command(CommandType.LEFT)), 
        ("RIGHT",Command(CommandType.RIGHT)), 
        ("REPORT", Command(CommandType.REPORT)),
    ])
    def test_parse_valid_one_part_commands(self, parser, command_str, expected):
        result = parser.parse(command_str)
        assert asdict(result) == asdict(expected)
    
    @pytest.mark.parametrize("command_str", [
        ("PLACE 12NORTH"),
        ("PLACE 33,EAST"),
        ("PLACE 100,100,WESTT"),
        ("PLACE 88,88,SOU"),
        ("PLACE AA,BB,EAST"),
        ("PLACE ABC"),
    ])
    def test_parse_place_with_invalid_arguments_raises_value_error(self, parser, command_str):
        with pytest.raises(ValueError):
            parser.parse(command_str)
            
    @pytest.mark.parametrize("command_str, expected", [
        ("PLACE 1,2,NORTH", Command(CommandType.PLACE, 1, 2, Direction.NORTH)),
        ("PLACE 3,4,SOUTH", Command(CommandType.PLACE, 3, 4, Direction.SOUTH)),
        ("PLACE 999,999,EAST", Command(CommandType.PLACE, 999, 999, Direction.EAST)),
        ("PLACE 34,34,WEST    ", Command(CommandType.PLACE, 34, 34, Direction.WEST)),
    ])
    def test_parse_valid_place_commands(self, parser, command_str, expected):
        result = parser.parse(command_str)
        assert asdict(result) == asdict(expected)