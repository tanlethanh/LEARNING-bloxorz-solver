from enum import Enum

from bloxorz.element.block import DoubleBlock
from bloxorz.element.game_board import GameBoard
from bloxorz.element.switch import TeleportSwitch, NormalSwitch
from aisolver.genetic.chromosome import Chromosome
from bloxorz.utils.maze_distance import maze_distance
from bloxorz.utils.manhattan_distance import manhattan_distance


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
        """
        Get the opposite action of current action left <-> right, up <-> down
        """
        if self != BlockAction.NONE and self.value != BlockAction.TOGGLE_FOCUSSING:
            return BlockAction(-self.value)


class BloxorzChromosome(Chromosome):

    DISTANCE_CALCULATION_TYPES = ["manhattan", "maze"]

    def __init__(self, dna, game_board: GameBoard, initial_position, list_initial_state,
                 distance_calculation_type="manhattan"):
        self.cross_index = None
        self.game_board = game_board
        self.initial_position = initial_position
        if list_initial_state is None:
            self.list_initial_state = []
        else:
            self.list_initial_state = list_initial_state

        self.distance_calculation_type = distance_calculation_type
        if self.distance_calculation_type == 1:
            pass
        elif self.distance_calculation_type == 2:
            # Use dict to optimize the routing calculation
            self.distance_dict = dict()

        super().__init__(dna, list(BlockAction))

    def take_valid_action(self, block: DoubleBlock, action: BlockAction, list_state, is_valid=None) -> int:
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
            # for get all valid action
            if is_valid is not None:
                is_valid["value"] = True
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
                distance = self.distance_fitness(block)
                if distance < min_distance:
                    min_distance = distance
                    self.cross_index = len(new_good_dna) - 1

        # restruct dna
        new_dna = new_good_dna + new_bad_dna
        self.DNA = new_dna

        distance = self.distance_fitness(block)
        self.fitness_score += distance

        return self.fitness_score

    def distance_fitness(self, block: DoubleBlock) -> int:
        """
        This function calculates distance from position of a block to goal position in the game board
        We have two type of calculation
        - Version 1: manhattan distance
        - Version 2: local optimize route - use BrFS with maze problem
        """
        first_position = block.first_block.get_position()
        second_position = block.second_block.get_position()
        list_position = [first_position, second_position]

        distance = 0
        if self.distance_calculation_type == "manhattan":
            for position in list_position:
                distance += manhattan_distance(position, self.game_board.get_goal_position())
            return distance

        elif self.distance_calculation_type == "maze":
            for position in list_position:
                if position in self.distance_dict:
                    distance += self.distance_dict[first_position]
                else:
                    distance += maze_distance(self.game_board, first_position,
                                              self.game_board.get_goal_position())
                    self.distance_dict.update({first_position: distance})
            return distance

        else:
            raise Exception("Version of distance calculation is invalid")

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

    def get_valid_action(self):
        block = DoubleBlock(self.initial_position)
        list_state = self.list_initial_state[:]
        result = []
        for action in self.DNA:
            is_valid = {
                "value": False
            }
            self.take_valid_action(block, action, list_state, is_valid)
            if is_valid["value"]:
                result.append(action)
        return result

    @staticmethod
    def is_valid_distance_calculation_type(cross_over_type):
        return cross_over_type in BloxorzChromosome.DISTANCE_CALCULATION_TYPES

    @staticmethod
    def all_distance_calculation_types():
        return BloxorzChromosome.DISTANCE_CALCULATION_TYPES[:]


