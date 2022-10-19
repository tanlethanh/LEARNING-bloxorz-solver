from bloxorz.block import DoubleBlock, DoubleBlockState
from bloxorz.switch import NormalSwitch, SwitchType, SwitchFunction, TeleportSwitch
from tile import Tile, TileType, BridgeState, Bridge


class GameBoard:

    def __init__(self, map_string, bridges_string):
        self.width = len(map_string)
        self.height = 0

        # Store bridges
        self.bridges = [[tuple(tile_position) for tile_position in bridge] for bridge in bridges_string]

        # Get map size
        for col in map_string:
            if len(col) > self.width:
                self.height = len(col)

        # Initialize map
        self.map = []
        list_switch = []
        for x_axis in range(0, self.width):
            map_col = []
            for y_axis in range(0, self.height):
                element = map_string[x_axis][y_axis]
                if isinstance(element, str):
                    match map_string[x_axis][y_axis]:
                        case "----":
                            map_col.append(Tile(x_axis, y_axis, state=TileType.OFF))
                        case "Tile":
                            map_col.append(Tile(x_axis, y_axis, state=TileType.ON))
                        case "Goal":
                            map_col.append(Tile(x_axis, y_axis, state=TileType.GOAL))
                        case "Orange":
                            map_col.append(Tile(x_axis, y_axis, state=TileType.ORANGE))
                        case _:
                            map_col.append(Tile(x_axis, y_axis, state=TileType.INVALID))
                elif isinstance(element, dict):
                    map_col.append(Tile(x_axis, y_axis, state=TileType.ON))
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
                first_tile = tuple(sw["object"]["tiles"][0])
                second_tile = tuple(sw["object"]["tiles"][1])
                first_tile = self.map[first_tile[0]][first_tile[1]]
                second_tile = self.map[second_tile[0]][second_tile[1]]
                self.map[x][y] = TeleportSwitch(x, y, SwitchType[sw["object"]["type"]], first_tile, second_tile)

    def is_goal(self, block):
        if (
                isinstance(block, DoubleBlock)
                and block.state == DoubleBlockState.STANDING
                and self.map[block.first_block.x_axis][block.second_block.y_axis] == TileType.GOAL
        ):
            return True
        return False

    def is_valid_position(self, block):
        if not isinstance(block, DoubleBlock):
            raise Exception(f"{block} is not a DoubleBlock!")

        try:
            first_tile_state = self.map[block.first_block.x_axis][block.first_block.y_axis].state
            second_tile_state = self.map[block.second_block.x_axis][block.second_block.y_axis].state
        except Exception as e:
            print(f"Out of map: {e}")
            return False

        match block.state:
            case DoubleBlockState.STANDING:
                if (
                        first_tile_state == TileType.OFF
                        or first_tile_state == TileType.INVALID
                        or first_tile_state == TileType.ORANGE
                ):
                    return False
                else:
                    return True

            case DoubleBlockState.LYING:
                if (
                    (first_tile_state == TileType.ORANGE and second_tile_state == TileType.ORANGE)
                    or
                    (first_tile_state == TileType.ON and second_tile_state == TileType)
                ):
                    return True
                return False

            case DoubleBlockState.DIVIDED:
                if first_tile_state == TileType.OFF or second_tile_state == TileType.OFF:
                    return False
                return True

    def update_map(self, list_state_all_bridge):
        for index, bridge_state in enumerate(list_state_all_bridge):
            for x_axis, y_axis in self.bridges[index].list_tile:
                current_tile = self.map[x_axis][y_axis]
                if (
                        bridge_state == BridgeState.ACTIVATED and current_tile.state == TileType.OFF
                        or
                        bridge_state == BridgeState.NOT_ACTIVE and current_tile.state == TileType.ON
                ):
                    current_tile.toggle()
