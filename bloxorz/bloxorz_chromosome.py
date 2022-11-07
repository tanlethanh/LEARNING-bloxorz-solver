from enum import Enum

from bloxorz.element.block import DoubleBlock
from bloxorz.element.game_board import GameBoard
from bloxorz.element.switch import TeleportSwitch, NormalSwitch
from aisolver.genetic.chromosome import Chromosome
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
        self.cross_index = None
        self.game_board = game_board
        self.initial_position = initial_position
        if list_initial_state is None:
            self.list_initial_state = []
        else:
            self.list_initial_state = list_initial_state
        super().__init__(dna, list(BlockAction))

    def take_valid_action(self, block: DoubleBlock, action: BlockAction, list_state) -> int:
        """
        This function take action to a block
        If position of block is not valid in the game board, reverse action of the block
        Return penalty score of this action
        """
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
        """
        This function calculate fitness score of a chromosome
        Fitness score = distance fitness + position penalty
        Best fitness score = Minimum fitness = 0
        """
        block = DoubleBlock(self.initial_position)
        list_state = self.list_initial_state[:]

        self.fitness_score = 0
        self.cross_index = 0

        new_good_dna = []
        new_bad_dna = []
        min_distance = 9999
        for action in self.DNA:
            penalty = self.take_valid_action(block, action, list_state)
            if penalty == 0:
                new_good_dna.append(action)
            else:
                new_bad_dna.append(action)

            if self.game_board.is_goal(block):
                self.DNA = new_good_dna + ([BlockAction.NONE] * (len(self.DNA) - len(new_good_dna)))
                self.fitness_score = 0
                return self.fitness_score

            self.fitness_score += penalty

            # Trigger the switch if it is possible
            if action != BlockAction.NONE and penalty == 0:
                self.trigger_switch(block, list_state)
                distance = self.distance_block_to_goal(block)
                if distance < min_distance:
                    min_distance = distance
                    self.cross_index = len(new_good_dna) - 1

        # restruct dna
        new_dna = new_good_dna + new_bad_dna
        self.DNA = new_dna

        distance = self.distance_block_to_goal(block)
        self.fitness_score += distance

        return self.fitness_score

    def distance_block_to_goal(self, block, version=1) -> int:
        """
        This function calculates distance from position of a block to goal position in the game board
        We have two version of calculation
        - Version 1: manhattan distance
        - Version 2: local optimize route - use BrFS with maze problem
        """
        if version == 1:
            distance_1 = manhattan_distance(
                (block.first_block.x_axis, block.first_block.y_axis),
                self.game_board.get_goal_position()
            )
            distance_2 = manhattan_distance(
                (block.second_block.x_axis, block.second_block.y_axis),
                self.game_board.get_goal_position()
            )
            return distance_1 + distance_2

    def trigger_switch(self, block, list_state):
        """
        This function triggers the switch if a block standing on a switch
        """
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





