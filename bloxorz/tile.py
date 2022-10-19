from enum import Enum


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

    def __init__(self, x_axis, y_axis, **kwargs):
        self.x_axis = x_axis
        self.y_axis = y_axis
        if kwargs["state"] == "on":
            self.state = TileType.ON
        elif kwargs["state"] == "off":
            self.state = TileType.OFF
        else:
            self.state = TileType.INVALID

    def toggle(self):
        if self.state == TileType.ON:
            self.state = TileType.OFF
        elif self.state == TileType.OFF:
            self.state = TileType.ON
        else:
            raise Exception("Can not toggle invalid Tile")

    def get_position(self):
        return self.x_axis, self.y_axis


class Bridge:
    def __int__(self, *args):
        self.list_tile = [tile for tile in args if isinstance(tile, Tile)]


