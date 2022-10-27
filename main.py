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

try:
    state_bridges = input_data["state_bridges"]
    state_bridges = [bool(state) for state in state_bridges]
except Exception as e:
    state_bridges = None

# Get AI algorithm
algorithm = sys.argv[2].upper()

frontier = None
if algorithm == "DFS":
    frontier = StackFrontier()

elif algorithm == "BFS":
    frontier = QueueFrontier()

game_solver = BlindSolver(frontier, game_board, initial_position, state_bridges)
res = game_solver.solve()
print(f"Number of discovered state: {len(game_solver.explored)}")
print(f"Number of step: {len(res)}")
print(res)

