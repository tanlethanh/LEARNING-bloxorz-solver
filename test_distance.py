import json
import sys

from bloxorz.block import DoubleBlock
from bloxorz.game_board import GameBoard
from bloxorz.tile import TileType
from distance_calculator import distance_between_two_positions

if len(sys.argv) != 2:
    print("arguments: [input file name]")
    sys.exit()

# Get data from json input file
input_file = "./input/" + sys.argv[1]
with open(input_file) as f:
    input_data = json.load(f)

# Create bloxorz game board and initial position
game_board = GameBoard(input_data["map"], input_data["bridges"])
# init position
initial_position = input_data["initial_position"]
initial_position = initial_position.split(" ")
initial_position = tuple(int(pos) for pos in initial_position)
game_board.map[initial_position[0]][initial_position[1]].state = TileType.GOAL

distance = distance_between_two_positions(game_board, initial_position, game_board.get_goal_position())

double_block = DoubleBlock(initial_position)
game_board.print_game_board(double_block)

print(distance)

