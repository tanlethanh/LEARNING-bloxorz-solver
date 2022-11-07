from enum import Enum

from multipledispatch import dispatch

from bloxorz.element.block import DoubleBlock, DoubleBlockState
from bloxorz.element.tile import Tile, TileType, Bridge


class SwitchType(Enum):
    SOFT = "SOFT"
    HEAVY = "HEAVY"


class SwitchFunction(Enum):
    OFF = "OFF"
    ON = "ON"
    TOGGLE = "TOGGLE"


class TeleportSwitch(Tile):

    @dispatch(int, int)
    def __init__(self, x_axis, y_axis):
        super().__init__(x_axis, y_axis, TileType.ON)
        self.first_tile = None
        self.second_tile = None

    @dispatch(int, int, Tile, Tile)
    def __init__(self, x_axis, y_axis, first_tile, second_tile):
        if not isinstance(first_tile, Tile) or not isinstance(second_tile, Tile):
            raise Exception("Some fields are invalid to initialize TeleportSwitch")
        else:
            super().__init__(x_axis, y_axis)
            self.first_tile = first_tile
            self.second_tile = second_tile

    @dispatch(DoubleBlock)
    def trigger(self, block):
        if (
                block.state == DoubleBlockState.STANDING
                and block.first_block.x_axis == self.x_axis
                and block.first_block.y_axis == self.y_axis
        ):
            block.first_block.set_position(self.first_tile.x_axis, self.first_tile.y_axis)
            block.second_block.set_position(self.second_tile.x_axis, self.second_tile.y_axis)
            block.state = DoubleBlockState.DIVIDED
            block.focussing = block.first_block
            print("")

        # else:
        #     raise Exception(f"can not trigger {block} by teleport switch {self}")


class NormalSwitch(Tile):
    bridges: list[Bridge]

    def __init__(self, x_axis, y_axis, sw_type, function, bridges):
        if isinstance(function, SwitchFunction) and isinstance(sw_type, SwitchType) and isinstance(bridges, list):
            for bridge in bridges:
                if not isinstance(bridge, Bridge):
                    raise Exception("List of bridge are invalid to initialize NormalSwitch")

            super().__init__(x_axis, y_axis, TileType.ON)
            self.type = sw_type
            self.function = function
            self.bridges = bridges
        else:
            raise Exception("Some fields are invalid to initialize NormalSwitch")

    @dispatch(DoubleBlock, list)
    def trigger(self, block, list_state_all_bridge):
        if self.is_matched_condition(block):
            list_index = self.get_all_index_of_bridges()
            if self.function == SwitchFunction.TOGGLE:
                for index in list_index:
                    list_state_all_bridge[index] = not list_state_all_bridge[index]

            elif self.function == SwitchFunction.ON:
                for index in list_index:
                    if not list_state_all_bridge[index]:
                        list_state_all_bridge[index] = not list_state_all_bridge[index]

            elif self.function == SwitchFunction.OFF:
                for index in list_index:
                    if list_state_all_bridge[index]:
                        list_state_all_bridge[index] = not list_state_all_bridge[index]

    @dispatch()
    def trigger(self):
        if self.function == SwitchFunction.TOGGLE:
            for bridge in self.bridges:
                for tile in bridge.list_tile:
                    tile.toggle()
        elif self.function == SwitchFunction.ON:
            for bridge in self.bridges:
                for tile in bridge.list_tile:
                    if tile.state == TileType.OFF:
                        tile.toggle()
        elif self.function == SwitchFunction.OFF:
            for bridge in self.bridges:
                for tile in bridge.list_tile:
                    if tile.state == TileType.ON:
                        tile.toggle()

    def get_all_index_of_bridges(self):
        list_index = []
        for bridge in self.bridges:
            list_index.append(bridge.index)
        return list_index

    def is_matched_condition(self, block):
        if not isinstance(block, DoubleBlock):
            raise Exception(f"This block {block} is invalid")
        return (
                # check condition of block to trigger this switch
                (
                    # condition of heavy switch
                    self.type == SwitchType.HEAVY
                    and block.state == DoubleBlockState.STANDING
                    and block.first_block.x_axis == self.x_axis
                    and block.first_block.y_axis == self.y_axis
                )
                or
                (
                    # condition of soft switch
                    self.type == SwitchType.SOFT
                    and (
                            (block.first_block.x_axis == self.x_axis and block.first_block.y_axis == self.y_axis)
                            or
                            (block.second_block.x_axis == self.x_axis and block.second_block.y_axis == self.y_axis)
                    )
                )
        )
