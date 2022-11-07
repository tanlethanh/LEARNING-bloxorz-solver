import json

from aisolver.blind.frontier import StackFrontier, QueueFrontier
from aisolver.blind.solver import Solver
from bloxorz.element.block import DoubleBlock
from bloxorz.element.game_board import GameBoard
from bloxorz.bloxorz_state import BloxorzState


class BloxorzSolver:

    @staticmethod
    def blind_solve(file_name, algorithm):
        with open(f"../input/{file_name}") as f:
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
            print(e)
            state_bridges = [False] * len(game_board.bridges)

        frontier = None
        if algorithm == "DFS":
            frontier = StackFrontier()

        elif algorithm == "BFS":
            frontier = QueueFrontier()

        initial_state = BloxorzState(DoubleBlock(initial_position), state_bridges, game_board)
        game_solver = Solver(frontier, initial_state)
        res = game_solver.solve()

        if res is not None:
            return [action.name for action in res]
        else:
            print("Cannot solve!")
            return None
