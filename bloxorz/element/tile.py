from enum import Enum

from multipledispatch import dispatch


class TileType(Enum):
    INVALID = 0
    ON = 1
    OFF = 2
    ORANGE = 3
    GOAL = 4


class BridgeState(Enum):
    ACTIVATED = True
    NOT_ACTIVE = False


class Tile:

    @dispatch(int, int, TileType)
    def __init__(self, x_axis, y_axis, state):
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.state = state
        self.count = 0

    def toggle(self):
        if self.state == TileType.ON:
            self.state = TileType.OFF
        elif self.state == TileType.OFF:
            self.state = TileType.ON
        else:
            raise Exception("Can not toggle invalid Tile")

    def get_position(self):
        return self.x_axis, self.y_axis


