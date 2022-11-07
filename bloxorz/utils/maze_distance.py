from enum import Enum

from aisolver.blind.frontier import QueueFrontier
from aisolver.blind.solver import Solver
from aisolver.blind.state import State
from bloxorz.element.game_board import GameBoard
from bloxorz.element.single_block import SingleBlock
from bloxorz.element.tile import TileType


class MazeStateAction(Enum):
    TURN_UP = 1
    TURN_RIGHT = 2
    TURN_DOWN = -1
    TURN_LEFT = -2


class MazeState(State):

    def __init__(self, block: SingleBlock, game_board: GameBoard, end_position, parent=None, parent_action=None)\
            -> None:
        super().__init__(parent, parent_action)
        self.goal_position = end_position
        self.block = block
        self.game_board = game_board

    def is_goal(self) -> bool:
        return self.block.get_position() == self.goal_position

    def neighbours(self) -> list:
        neighbours = []
        for action in MazeStateAction:
            new_block = SingleBlock(self.block)
            if action == MazeStateAction.TURN_UP:
                new_block.move_up()
            elif action == MazeStateAction.TURN_DOWN:
                new_block.move_down()
            elif action == MazeStateAction.TURN_RIGHT:
                new_block.move_right()
            elif action == MazeStateAction.TURN_LEFT:
                new_block.move_left()

            try:
                tile = self.game_board.map[new_block.x_axis][new_block.y_axis]
                if tile.state != TileType.OFF:
                    new_state = MazeState(new_block, self.game_board, self.goal_position, self, action)
                    neighbours.append(new_state)

            except Exception as e:
                # print(e)
                continue

        return neighbours

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, MazeState):
            return False
        return self.block.get_position() == o.block.get_position()


def maze_distance(game_board: GameBoard, start_position: tuple, end_position: tuple) -> int:
    """
    This function calculate distance like maze problem for Bloxorz
    The moving element is a SingleBlock
    Assumption: all bridges are ON state, skip the switches and goal position
    :param game_board: Bloxorz game board
    :param start_position: tuple (x, y)
    :param end_position: tuple (x, y)
    :return: maze distance from start position to end position
    """
    # turn on all bridges
    for bridge in game_board.bridges:
        bridge.turn_on()

    # init BrFS solver
    block = SingleBlock(start_position[0], start_position[1])
    frontier = QueueFrontier()
    initial_state = MazeState(block, game_board, end_position)
    blind_solver = Solver(frontier, initial_state)

    # solve and return distance
    res = blind_solver.solve()
    if res is not None:
        return len(res)
    return 9999
