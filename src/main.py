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
from command import Command, CommandType
from output import Report

def print_report(report: Report):
    print(f"Output: {report.x},{report.y},{report.direction.name}")

def main(file_path: str):
    parser = CommandParser()
    robot = Robot()
        
    # Validates all commands in command file before execution 
    try:
        commands: list[Command] = []
        with open(file_path, "r") as command_file:
            for command_line in command_file:
                command = parser.parse(command_line)
                commands.append(command)
        for command in commands:
            output = robot.execute(command)
            if output.command_ran == CommandType.REPORT and output.report:
                print_report(output.report)
    except ValueError as e:
        print(f"ERROR: {str(e)}")
            
if __name__ == "__main__":
    import argparse
    import os
    
    args_parser = argparse.ArgumentParser(description="Run robot using command file.")
    args_parser.add_argument("file_path", type=str, help="Path to command file to run.")
    args = args_parser.parse_args()
    
    file_path = args.file_path
    
    if os.path.isfile(file_path):
        main(file_path)
    else:
        print(f"ERROR: File '{file_path}' not found.")