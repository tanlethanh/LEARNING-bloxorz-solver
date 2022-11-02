from multipledispatch import dispatch

from bloxorz.block import DoubleBlock, DoubleBlockState
from bloxorz.switch import NormalSwitch, SwitchType, SwitchFunction, TeleportSwitch
from bloxorz.tile import Tile, TileType, BridgeState, Bridge


class GameBoard:

    def __init__(self, map_string, bridges_string):
        self.width = len(map_string)
        self.height = 0

        # Store bridges
        self.bridges = []
        for bridge in bridges_string:
            list_tile_index = []
            for tile_position in bridge:
                tile_position = tile_position.split(" ")
                list_tile_index.append((int(tile_position[0]), int(tile_position[1])))
            self.bridges.append(list_tile_index)

        # Get map size
        for col in map_string:
            if len(col) > self.height:
                self.height = len(col)

        # Initialize map
        self.map = []
        list_switch = []
        for x_axis in range(0, self.width):
            map_col = []
            for y_axis in range(0, self.height):
                element = map_string[x_axis][y_axis]
                if isinstance(element, str):
                    if element == "-":
                        map_col.append(Tile(x_axis, y_axis, TileType.OFF))
                    elif element == "T":
                        map_col.append(Tile(x_axis, y_axis, TileType.ON))
                    elif element == "G":
                        self.goal_tile = Tile(x_axis, y_axis, TileType.GOAL)
                        map_col.append(self.goal_tile)

                    elif element == "O":
                        map_col.append(Tile(x_axis, y_axis, TileType.ORANGE))
                    else:
                        map_col.append(Tile(x_axis, y_axis, TileType.INVALID))
                elif isinstance(element, dict):
                    map_col.append(Tile(x_axis, y_axis, TileType.ON))
                    list_switch.append({
                        "position": (x_axis, y_axis),
                        "object": element
                    })
            self.map.append(map_col)

        # Initialize list of bridge
        self.bridges = [
            Bridge(index, [self.map[x][y] for (x, y) in bridge])
            for index, bridge in enumerate(self.bridges)
        ]

        # Initialize all switch
        for sw in list_switch:
            x = sw["position"][0]
            y = sw["position"][1]
            if sw["object"]["sw_type"] == "NORMAL":
                self.map[x][y] = NormalSwitch(
                    x,
                    y,
                    SwitchType[sw["object"]["type"]],
                    SwitchFunction[sw["object"]["function"]],
                    [bridge for index, bridge in enumerate(self.bridges) if index in sw["object"]["bridges"]]
                )

            elif sw["object"]["sw_type"] == "TELEPORT":
                tiles = sw["object"]["tiles"]
                first_tile = [int(pos) for pos in tiles[0].split(" ")]
                second_tile = [int(pos) for pos in tiles[1].split(" ")]
                self.map[x][y] = current_tile = TeleportSwitch(x, y)
                first_tile = self.map[first_tile[0]][first_tile[1]]
                second_tile = self.map[second_tile[0]][second_tile[1]]
                current_tile.first_tile = first_tile
                current_tile.second_tile = second_tile

        self.print_game_board()

    def is_goal(self, block):
        try:
            current_tile = self.map[block.first_block.x_axis][block.second_block.y_axis]
        except Exception as e:
            print(f"Is goal: {e}")
            return False

        if (
                isinstance(block, DoubleBlock)
                and block.state == DoubleBlockState.STANDING
                and current_tile.state == TileType.GOAL
        ):
            return True
        return False

    def get_goal_position(self) -> tuple:
        return self.goal_tile.x_axis, self.goal_tile.y_axis

    def is_valid_position(self, block):
        if not isinstance(block, DoubleBlock):
            raise Exception(f"{block} is not a DoubleBlock!")

        try:
            if (
                    block.first_block.x_axis < 0
                    or block.second_block.x_axis < 0
                    or block.first_block.y_axis < 0
                    or block.second_block.y_axis < 0
            ):
                raise Exception("Index is negative")
            first_tile_state = self.map[block.first_block.x_axis][block.first_block.y_axis].state
            second_tile_state = self.map[block.second_block.x_axis][block.second_block.y_axis].state
        except Exception as e:
            # print(f"Out of map: {e}")
            return False

        if block.state == DoubleBlockState.STANDING:
            if (
                    first_tile_state == TileType.OFF
                    or first_tile_state == TileType.INVALID
                    or first_tile_state == TileType.ORANGE
            ):
                return False
            else:
                return True

        elif block.state == DoubleBlockState.LYING:
            if first_tile_state == TileType.OFF or second_tile_state == TileType.OFF:
                return False
            return True

        elif block.state == DoubleBlockState.DIVIDED:
            if first_tile_state == TileType.OFF or second_tile_state == TileType.OFF:
                return False
            return True

    def update_map(self, list_state_all_bridge):
        for index, bridge_state in enumerate(list_state_all_bridge):
            for current_tile in self.bridges[index].list_tile:
                if (
                        (bridge_state == BridgeState.ACTIVATED.value and current_tile.state == TileType.OFF)
                        or
                        (bridge_state == BridgeState.NOT_ACTIVE.value and current_tile.state == TileType.ON)
                ):
                    current_tile.toggle()

    @dispatch()
    def print_game_board(self):
        for y in range(0, self.height).__reversed__():
            for x in range(0, self.width):
                current_tile = self.map[x][y]
                if isinstance(current_tile, NormalSwitch):
                    print("^", end="")
                elif isinstance(current_tile, TeleportSwitch):
                    print("%", end="")
                elif isinstance(current_tile, Tile):
                    if current_tile.state == TileType.ON:
                        print("*", end="")
                    elif current_tile.state == TileType.OFF:
                        print(" ", end="")
                    elif current_tile.state == TileType.ORANGE:
                        print("-", end="")
                    elif current_tile.state == TileType.GOAL:
                        print("X", end="")
            print("")

    @dispatch(DoubleBlock)
    def print_game_board(self, block):
        for y in range(0, self.height).__reversed__():
            for x in range(0, self.width):
                current_tile = self.map[x][y]
                if (
                        (
                                current_tile.x_axis == block.first_block.x_axis and current_tile.y_axis == block.first_block.y_axis)
                        or
                        (
                                current_tile.x_axis == block.second_block.x_axis and current_tile.y_axis == block.second_block.y_axis)
                ):
                    print("=", end="")
                elif isinstance(current_tile, NormalSwitch):
                    print("^", end="")
                elif isinstance(current_tile, TeleportSwitch):
                    print("%", end="")
                elif isinstance(current_tile, Tile):
                    if current_tile.state == TileType.ON:
                        print("*", end="")
                    elif current_tile.state == TileType.OFF:
                        print(" ", end="")
                    elif current_tile.state == TileType.ORANGE:
                        print("-", end="")
                    elif current_tile.state == TileType.GOAL:
                        print("X", end="")
            print("")
