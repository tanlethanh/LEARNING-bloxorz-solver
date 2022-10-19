from enum import Enum
from bloxorz.block import DoubleBlock, DoubleBlockState


class Action(Enum):
    TURN_LEFT = 0
    TURN_RIGHT = 1
    TURN_UP = 2
    TURN_DOWN = 3
    TOGGLE_FOCUSSING = 4

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class State:

    def __init__(self, block, list_state_all_bridge, parent_state=None, parent_action=None):

        if (
                not isinstance(block, DoubleBlock)
                or not isinstance(list_state_all_bridge, list)
                or (parent_state is not None and not isinstance(parent_state, State))
                or (parent_action is not None and not isinstance(parent_action, Action))
        ):
            raise Exception("Some fields are not valid to initialize a State")

        self.block = block
        self.list_state_all_bridge = list_state_all_bridge
        self.parent_state = parent_state
        self.parent_action = parent_action

    def equals(self, item):
        if not isinstance(item, State):
            return False
        return (
                self.block.equals(item.block)
                and self.list_state_all_bridge == item.list_state_all_bridge
        )

    def turn_up(self, bloxorz_map):
        self.block.move_up()

    def turn_down(self, bloxorz_map):
        self.block.move_down()

    def turn_left(self, bloxorz_map):
        self.block.move_left()

    def turn_right(self, bloxorz_map):
        self.block.move_right()

    def toggle_focussing(self, bloxorz_map):
        self.block.toggle_focussing()
