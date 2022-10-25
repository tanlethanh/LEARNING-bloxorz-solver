from enum import Enum
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

    @classmethod
    def list(cls):
        return list(map(lambda c: c, cls))


class State:

    list_state_all_bridge: list

    def __init__(self, block, list_state_all_bridge, parent_state=None, parent_action=None):

        if (
                not isinstance(block, DoubleBlock)
                or not isinstance(list_state_all_bridge, list)
                or (parent_state is not None and not isinstance(parent_state, State))
                or (parent_action is not None and not isinstance(parent_action, Action))
        ):
            raise Exception("Some fields are not valid to initialize a State")

        self.block = block
        self.list_state_all_bridge = list_state_all_bridge[:]
        self.parent_state = parent_state
        self.parent_action = parent_action

    def __eq__(self, other):
        if not isinstance(other, State):
            return False
        return (
                self.block.equals(other.block)
                and self.list_state_all_bridge == other.list_state_all_bridge
        )

    def __str__(self) -> str:
        return f"{self.block} <-> {self.list_state_all_bridge}\n"

    def equals(self, item):
        if not isinstance(item, State):
            return False
        return (
                self.block.equals(item.block)
                and self.list_state_all_bridge == item.list_state_all_bridge
        )

    def move(self, game_board, action) -> bool:
        if not isinstance(game_board, GameBoard):
            raise Exception("Game board is invalid")

        match action:
            case Action.TURN_UP:
                self.block.move_up()
            case Action.TURN_DOWN:
                self.block.move_down()
            case Action.TURN_LEFT:
                self.block.move_left()
            case Action.TURN_RIGHT:
                self.block.move_right()
            case Action.TOGGLE_FOCUSSING:
                self.block.toggle_focussing()

        if not game_board.is_valid_position(self.block):
            return False
        set_tile = set()
        try:
            first_tile = game_board.map[self.block.first_block.x_axis][self.block.first_block.y_axis]
            second_tile = game_board.map[self.block.second_block.x_axis][self.block.second_block.y_axis]
            if not isinstance(first_tile, Tile) or not isinstance(second_tile, Tile):
                x = self.block.first_block.x_axis
                y = self.block.first_block.y_axis
                raise Exception(f"Invalid tile at position ({x}, {y})")
            else:
                set_tile.add(first_tile)
                set_tile.add(second_tile)
        except Exception as e:
            print(f"Get off the game board: {e}")
            return False

        for tile in set_tile:
            if isinstance(tile, TeleportSwitch):
                tile.trigger(self.block)
            elif isinstance(tile, NormalSwitch):
                tile.trigger(self.block, self.list_state_all_bridge)
        return True
