# Toy Robot Simulator

This program simulates a toy robot moving on a 5x5 grid based on a series of commands.

## Environment

- **Grid Size**: 5x5 (0,0 is the bottom-left corner, 4,4 is the top-right corner)
- **Obstructions**: None (the grid is open and unobstructed)

## Commands

- **PLACE X,Y,F**
  - Places the robot on the grid at the specified coordinates `(X, Y)` facing the direction `F`.
  - Example: `PLACE 2,3,NORTH`
  - Valid directions (`F`): `NORTH`, `EAST`, `SOUTH`, `WEST`
  
- **MOVE**
  - Moves the robot one unit forward in the direction it is currently facing.

- **LEFT**
  - Rotates the robot 90 degrees counterclockwise (left).

- **RIGHT**
  - Rotates the robot 90 degrees clockwise (right).

- **REPORT**
  - Outputs the current position and direction of the robot.
  - Example: `Output: 2,3,NORTH`

## Constraints

- The first valid command must be `PLACE`. Any commands before the first `PLACE` command are ignored.
- The `PLACE` command can be used multiple times to reposition the robot.
- The robot cannot move outside the grid boundaries. Any commands that would cause the robot to "fall" off the grid are ignored, including the `PLACE` command if the coordinates are outside the grid.

## Getting Started

### Setup

To run pytest, you need to install the required packages. Use the following command to install them:

```bash
pip install -r requirements.txt
```

### Running Tests
Unit tests are provided using pytest. To run the tests, execute the following command:
```bash
pytest
```

### Runing the Program

To run the program with a set of commands from a file, use the following command:
```bash
python src/main.py path_to_file.txt
```