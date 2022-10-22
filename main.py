import json
import sys

from blind_solver import BlindSolver
from frontier import StackFrontier, QueueFrontier
from bloxorz.game_board import GameBoard

if len(sys.argv) != 3:
    print("exit")
    sys.exit()

# Get data from json input file
input_file = "./input/" + sys.argv[1]
with open(input_file) as f:
    input_data = json.load(f)

# Create bloxorz game board and initial position
game_board = GameBoard(input_data["map"], input_data["bridges"])
initial_position = input_data["initial_position"]
initial_position = initial_position.split(" ")
initial_position = tuple(int(pos) for pos in initial_position)

# Get AI algorithm
algorithm = sys.argv[2].upper()

if algorithm == "DFS":
    stack_frontier = StackFrontier()
    game_solver = BlindSolver(stack_frontier, game_board, initial_position)
    res = game_solver.solve()
    print(res)

elif algorithm == "BFS":
    queue_frontier = QueueFrontier()
    game_solver = BlindSolver(queue_frontier, game_board, initial_position)
    res = game_solver.solve()
    print(res)

