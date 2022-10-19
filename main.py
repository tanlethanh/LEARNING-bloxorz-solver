import json
import sys

from blind_solver import BlindSolver
from frontier import StackFrontier, QueueFrontier
from bloxorz.game_board import GameBoard

if len(sys.argv) != 4:
    print("exit")
    sys.exit()

# Get data from json input file
input_file = sys.argv[1]
with open(input_file) as f:
    input_data = json.load(f)

# Create bloxorz game board and initial position
game_board = GameBoard(input_data["map"], input_data["bridges"])
initial_position = input_data["initial_position"]

# Get AI algorithm
algorithm = sys.argv[2].upper()

if algorithm == "DFS":
    stack_frontier = StackFrontier()
    game_solver = BlindSolver(stack_frontier, game_board, initial_position)

elif algorithm == "BFS":
    queue_frontier = QueueFrontier()
    game_solver = BlindSolver(queue_frontier, game_board, initial_position)


