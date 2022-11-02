from enum import Enum

from bloxorz.block import DoubleBlock
from bloxorz.game_board import GameBoard
from bloxorz.switch import TeleportSwitch, NormalSwitch
from genetic_solver import Chromosome
from utils import manhattan_distance


class BlockAction(Enum):
    NONE = 0
    TURN_UP = 1
    TURN_DOWN = -1
    TURN_LEFT = 2
    TURN_RIGHT = -2
    TOGGLE_FOCUSSING = 3

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other):
        if not isinstance(other, BlockAction):
            return False
        return self.value == other.value

    def opposite_action(self):
        if self != BlockAction.NONE and self.value != BlockAction.TOGGLE_FOCUSSING:
            return BlockAction(-self.value)


class BloxorzChromosome (Chromosome):

    def __init__(self, dna, game_board: GameBoard, initial_position, list_initial_state):
        self.game_board = game_board
        self.initial_position = initial_position
        if list_initial_state is None:
            self.list_initial_state = []
        else:
            self.list_initial_state = list_initial_state
        super().__init__(dna, list(BlockAction))

    # This function take action to a block
    # If position of block is not valid in the game board, reverse action of the block
    # Return penalty score of this action
    def take_valid_action(self, block: DoubleBlock, action: BlockAction, list_state) -> int:
        try:
            if action == BlockAction.NONE:
                return 0
            elif action == BlockAction.TURN_UP:
                block.move_up()
            elif action == BlockAction.TURN_DOWN:
                block.move_down()
            elif action == BlockAction.TURN_LEFT:
                block.move_left()
            elif action == BlockAction.TURN_RIGHT:
                block.move_right()
            elif action == BlockAction.TOGGLE_FOCUSSING:
                block.toggle_focussing()
        except Exception as e:
            # print(e)
            return 0

        self.game_board.update_map(list_state)
        if self.game_board.is_valid_position(block):
            return 0
        else:
            self.take_valid_action(block, action.opposite_action(), list_state)
            return 1

    def calculate_fitness(self):

        block = DoubleBlock(self.initial_position)
        list_state = self.list_initial_state[:]

        self.fitness_score = 0

        for action in self.DNA:
            penalty = self.take_valid_action(block, action, list_state)
            self.fitness_score += penalty

            # Trigger the switch if it is possible
            if action != BlockAction.NONE and penalty == 0:
                first_tile = self.game_board.map[block.first_block.x_axis][block.first_block.y_axis]
                second_tile = self.game_board.map[block.second_block.x_axis][block.second_block.y_axis]
                tiles = [first_tile]
                if first_tile != second_tile:
                    tiles.append(second_tile)

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
        return self.fitness_score




