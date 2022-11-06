from enum import Enum

from aisolver.blind.state import State
from bloxorz.block import DoubleBlock
from bloxorz.game_board import GameBoard
from bloxorz.switch import TeleportSwitch, NormalSwitch
from bloxorz.tile import Tile


class Action(Enum):
    TURN_LEFT = "TURN_LEFT"
    TURN_RIGHT = "TURN_RIGHT"
    TURN_UP = "TURN_UP"
    TURN_DOWN = "TURN_DOWN"
    TOGGLE_FOCUSSING = "TOGGLE_FOCUSSING"

    def __str__(self) -> str:
        return self.name


class BloxorzState(State):

    list_state_all_bridge: list
    game_board: GameBoard
    block: DoubleBlock

    def __init__(self, block, list_state, game_board, parent_state=None, parent_action=None):

        if (
                not isinstance(block, DoubleBlock)
                or not isinstance(list_state, list)
                or (parent_state is not None and not isinstance(parent_state, BloxorzState))
                or (parent_action is not None and not isinstance(parent_action, Action))
        ):
            raise Exception("Some fields are not valid to initialize a State")

        super().__init__(parent_state, parent_action)
        self.block = block
        self.list_state_all_bridge = list_state[:]
        self.game_board = game_board

    def __eq__(self, other):
        if not isinstance(other, BloxorzState):
            return False
        return (
                self.block == other.block
                and self.list_state_all_bridge == other.list_state_all_bridge
        )

    def __str__(self) -> str:
        return f"{self.block} <-> {self.list_state_all_bridge}\n"

    def print_game_state(self):
        print(f"Parent state: {self.parent}\t -- {self.parent_action} --> {self}")
        self.game_board.update_map(self.list_state_all_bridge)
        self.game_board.print_game_board(self.block)
        print("-------------------------------------------------")

    def is_goal(self) -> bool:
        self.game_board.update_map(self.list_state_all_bridge)
        return self.game_board.is_goal(self.block)

    def neighbours(self) -> list:
        neighbours = []
        for action in Action:
            # create child state from current state, not yet take action
            new_state = BloxorzState(DoubleBlock(self.block), self.list_state_all_bridge, self.game_board, self, action)
            is_valid_state = new_state.take_action(action)
            if is_valid_state:
                neighbours.append(new_state)
                # new_state.print_game_state()
        return neighbours

    def take_action(self, action) -> bool:
        # Move block when take action to current state
        # Block moving can throw exception if state of block is not met
        try:
            if action == Action.TURN_UP:
                self.block.move_up()
            elif action == Action.TURN_DOWN:
                self.block.move_down()
            elif action == Action.TURN_LEFT:
                self.block.move_left()
            elif action == Action.TURN_RIGHT:
                self.block.move_right()
            elif action == Action.TOGGLE_FOCUSSING:
                self.block.toggle_focussing()
        except:
            return False

        # Check position of block in the game board
        self.game_board.update_map(self.list_state_all_bridge)
        if not self.game_board.is_valid_position(self.block):
            return False

        # Trigger the switch if it's possible
        try:
            tiles = []
            x_1, y_1 = self.block.first_block.get_position()
            x_2, y_2 = self.block.second_block.get_position()
            tile_1 = self.game_board.map[x_1][y_1]
            tile_2 = self.game_board.map[x_2][y_2]
            tiles.append(tile_1)
            if tile_2 != tile_1:
                tiles.append(tile_2)
            for tile in tiles:
                if isinstance(tile, TeleportSwitch):
                    tile.trigger(self.block)
                elif isinstance(tile, NormalSwitch):
                    tile.trigger(self.block, self.list_state_all_bridge)
                    # print(f"Trigger {tile.x_axis, tile.y_axis}")
        except Exception as e:
            print(f"Get off the game board: {e}")
            return False

        return True


