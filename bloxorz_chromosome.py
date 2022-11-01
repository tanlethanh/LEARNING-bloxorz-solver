from enum import Enum

from bloxorz.block import DoubleBlock
from bloxorz.game_board import GameBoard
from bloxorz.switch import TeleportSwitch, NormalSwitch
from genetic_solver import Chromosome
from utils import manhattan_distance


class BlockAction(Enum):
    NONE = "NONE"
    TURN_UP = "TURN_UP"
    TURN_DOWN = "TURN_DOWN"
    TURN_LEFT = "TURN_LEFT"
    TURN_RIGHT = "TURN_RIGHT"
    TOGGLE_FOCUSSING = "TOGGLE_FOCUSSING"

    def __str__(self) -> str:
        return self.name


class BloxorzChromosome (Chromosome):

    def __init__(self, dna, game_board: GameBoard, initial_position, list_initial_state):
        self.game_board = game_board
        self.initial_position = initial_position
        if list_initial_state is None:
            self.list_initial_state = []
        else:
            self.list_initial_state = list_initial_state
        super().__init__(dna, list(BlockAction))

    def calculate_fitness(self):

        block = DoubleBlock(self.initial_position)
        list_state = self.list_initial_state[:]

        self.fitness_score = 0

        for ele in self.DNA:
            if ele == BlockAction.NONE:
                continue
            elif ele == BlockAction.TURN_UP:
                block.move_up()
            elif ele == BlockAction.TURN_DOWN:
                block.move_down()
            elif ele == BlockAction.TURN_LEFT:
                block.move_left()
            elif ele == BlockAction.TURN_RIGHT:
                block.move_right()
            elif ele == BlockAction.TOGGLE_FOCUSSING:
                block.toggle_focussing()

            self.game_board.update_map(list_state)
            if not self.game_board.is_valid_position(block):
                self.fitness_score += 1
            else:
                first_tile = self.game_board.map[block.first_block.x_axis][block.first_block.y_axis]
                second_tile = self.game_board.map[block.second_block.x_axis][block.second_block.y_axis]
                tiles = [first_tile, second_tile]
                for tile in tiles:
                    if isinstance(tile, TeleportSwitch):
                        tile.trigger(block)
                    elif isinstance(tile, NormalSwitch):
                        tile.trigger(block, list_state)

        distance_1 = manhattan_distance(
            (block.first_block.x_axis, block.first_block.y_axis),
            self.game_board.get_goal_position()
        )

        distance_2 = manhattan_distance(
            (block.second_block.x_axis, block.second_block.y_axis),
            self.game_board.get_goal_position()
        )

        self.fitness_score += distance_1 + distance_2




