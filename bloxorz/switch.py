from enum import Enum
from tile import Tile, TileType, Bridge


class SwitchType(Enum):
    SOFT = 1
    HEAVY = 2


class SwitchFunction(Enum):
    TO_TURN_OFF = 0
    TO_TURN_ON = 1
    TO_TOGGLE = 2


class Switch(Tile):

    def __init__(self, x_axis, y_axis, sw_type):
        if isinstance(sw_type, SwitchType):
            super().__init__(x_axis, y_axis)
            self.type = sw_type
        else:
            raise Exception("Type of switch is not valid")


class TeleportSwitch(Switch):

    def __int__(self, x_axis, y_axis, sw_type):
        super().__init__(sw_type, x_axis, y_axis)
        self.first_tile = None
        self.second_tile = None

    def __init__(self, x_axis, y_axis, sw_type, first_tile, second_tile):
        if not isinstance(first_tile, Tile) or not isinstance(second_tile, Tile):
            raise Exception("Tiles are not valid")
        else:
            super().__init__(sw_type, x_axis, y_axis)
            self.first_tile = first_tile
            self.second_tile = second_tile

    def get_split_position(self):
        if self.first_tile.state == TileType.ON and self.second_tile.state == TileType.ON:
            return self.first_tile.get_position(), self.second_tile.get_position()


class NormalSwitch(Switch):

    def __int__(self, x_axis, y_axis, sw_type, function, bridge):
        if isinstance(function, SwitchFunction) and isinstance(sw_type, SwitchType) and isinstance(bridge, Bridge):
            super().__init__(x_axis, y_axis, sw_type)
            self.function = function
            self.bridge = bridge
        else:
            raise Exception("aa")

    def trigger(self):
        match self.function:
            case SwitchFunction.TO_TOGGLE:
                for tile in self.bridge.list_tile:
                    tile.toggle()
            case SwitchFunction.TO_TURN_ON:
                for tile in self.bridge.list_tile:
                    if tile.state == TileType.ON:
                        return
                for tile in self.bridge.list_tile:
                    tile.toggle()
            case SwitchFunction.TO_TURN_OFF:
                for tile in self.bridge.list_tile:
                    if tile.state == TileType.OFF:
                        return
                for tile in self.bridge.list_tile:
                    tile.toggle()

