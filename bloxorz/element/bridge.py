from bloxorz.element.tile import Tile, TileType


class Bridge:

    list_tile: list[Tile]

    def __init__(self, index, list_tile):
        self.list_tile = [tile for tile in list_tile if isinstance(tile, Tile)]
        self.index = index

    def turn_on(self):
        for tile in self.list_tile:
            tile.state = TileType.ON
