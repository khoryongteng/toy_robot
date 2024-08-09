import pytest
from src.robot import Robot

@pytest.fixture
def robot():
    return Robot()
 
class TestRobot:
    def test_xxx(self, robot):
        assert isinstance(robot, Robot)