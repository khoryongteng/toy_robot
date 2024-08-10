# Starting Notes:
# Program takes in Commands which Moves a robot on the grid
# 
# Environment: 5x5 Grid. No Obstructions
#
# Commands:
# PLACE X,Y,F (Example: PLACE 2,3,NORTH)
# MOVE: Move the robot one unit forward in the direction it is facing.
# LEFT: Rotate -90 degrees
# RIGHT: Rotate +90 degrees
# REPORT: (Prints: Output: X,Y,F)
#
# Constraints:
# First Valid command is PLACE, any commands before the first PLACE are ignored.
# PLACE can be used multiple times.
# The robot should not move outside the grid boundaries ("Fall"). "Fall" commands are ignored. (Including PLACE)

from command_parser import CommandParser
from robot import Robot
from command import CommandType

def main():
    parser = CommandParser()
    robot = Robot()

    try:
        while True:
            user_input = input("Enter command: \n")
            command = parser.parse(user_input)
            output = robot.execute(command)
            if output.command_ran == CommandType.REPORT and output.report:
                print(f"Output: {output.report.x},{output.report.y},{output.report.direction.name}")
    except ValueError as e:
        print(f"ERROR: {str(e)}")
            
if __name__ == "__main__":
    main()