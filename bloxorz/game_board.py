from bloxorz.block import DoubleBlock, DoubleBlockState
from tile import Tile, TileType, BridgeState


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
        for x_axis in range(0, self.width):
            map_col = []
            for y_axis in range(0, self.height):
                match map_string[x_axis][y_axis]:
                    case "----":
                        map_col.append(Tile(x_axis, y_axis, state=TileType.OFF))
                    case "Tile":
                        map_col.append(Tile(x_axis, y_axis, state=TileType.ON))
                    case "Goal":
                        map_col.append(Tile(x_axis, y_axis, state=TileType.GOAL))

            self.map.append(map_col)

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
            for x_axis, y_axis in self.bridges[index]:
                current_tile = self.map[x_axis][y_axis]
                if (
                        bridge_state == BridgeState.ACTIVATED and current_tile.state == TileType.OFF
                        or
                        bridge_state == BridgeState.NOT_ACTIVE and current_tile.state == TileType.ON
                ):
                    current_tile.toggle()
