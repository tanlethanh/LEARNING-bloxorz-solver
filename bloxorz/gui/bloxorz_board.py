import sys
from tkinter import Canvas, NW

from PIL import Image, ImageTk

from bloxorz.element.block import DoubleBlock
from bloxorz.element.game_board import GameBoard
from bloxorz.element.switch import NormalSwitch, TeleportSwitch, SwitchType
from bloxorz.element.tile import TileType


class BloxorzBoard(Canvas):
    TILE_SIZE = 40

    def __init__(self, master):
        super().__init__(master=master, width=900, height=500, borderwidth=0, highlightthickness=0)
        self.pack(padx=20, pady=20)
        self.create_rectangle(0, 0, 900, 500, outline="black", fill="white")
        self.load_images()

    def reset_game(self, game_board: GameBoard, block: DoubleBlock, list_state):
        self.game_board = game_board
        self.block = block
        self.list_state = list_state
        board_height = game_board.height * BloxorzBoard.TILE_SIZE
        board_width = game_board.width * BloxorzBoard.TILE_SIZE
        self.pad_x = (self.winfo_width() - board_width) / 2
        self.pad_y = (self.winfo_height() - board_height) / 2
        self.delete("all")
        self.init_game()

    def init_game(self):
        self.create_objects()

    def load_images(self):
        try:
            self.i_normal_tile = Image.open("images/normal-tile-v3.png") \
                .resize(size=(BloxorzBoard.TILE_SIZE, BloxorzBoard.TILE_SIZE))
            self.normal_tile = ImageTk.PhotoImage(self.i_normal_tile)

            self.i_orange_tile = Image.open("images/orange-tile.png") \
                .resize(size=(BloxorzBoard.TILE_SIZE, BloxorzBoard.TILE_SIZE))
            self.orange_tile = ImageTk.PhotoImage(self.i_orange_tile)

            self.i_normal_switch = Image.open("images/normal-sw-v2.png") \
                .resize(size=(BloxorzBoard.TILE_SIZE, BloxorzBoard.TILE_SIZE))
            self.normal_switch = ImageTk.PhotoImage(self.i_normal_switch)

            self.i_heavy_switch = Image.open("images/heavy-switch-v2.png") \
                .resize(size=(BloxorzBoard.TILE_SIZE, BloxorzBoard.TILE_SIZE))
            self.heavy_switch = ImageTk.PhotoImage(self.i_heavy_switch)

            self.i_teleport_switch = Image.open("images/teleport-switch.png") \
                .resize(size=(BloxorzBoard.TILE_SIZE, BloxorzBoard.TILE_SIZE))
            self.teleport_switch = ImageTk.PhotoImage(self.i_teleport_switch)

            self.i_single_block = Image.open("images/single-block-v2.png") \
                .resize(size=(BloxorzBoard.TILE_SIZE, BloxorzBoard.TILE_SIZE))
            self.single_block = ImageTk.PhotoImage(self.i_single_block)

        except IOError as e:
            print(e)
            sys.exit(1)

    def create_objects(self):
        for col in self.game_board.map:
            for ele in col:
                x, y = self.map_position(ele.x_axis, ele.y_axis)
                if isinstance(ele, TeleportSwitch):
                    self.create_image(x, y, image=self.teleport_switch, tag="teleport_switch", anchor=NW)
                elif isinstance(ele, NormalSwitch):
                    if ele.type == SwitchType.HEAVY:
                        self.create_image(x, y, image=self.heavy_switch, tag="heavy_switch", anchor=NW)
                    else:
                        self.create_image(x, y, image=self.normal_switch, tag="normal_switch", anchor=NW)
                elif ele.state == TileType.ON:
                    self.create_image(x, y, image=self.normal_tile, tag="normal_tile", anchor=NW)
                elif ele.state == TileType.ORANGE:
                    self.create_image(x, y, image=self.orange_tile, tag="orange_tile", anchor=NW)

        for (index, state) in enumerate(self.list_state):
            for (tile_index, tile) in enumerate(self.game_board.bridges[index].list_tile):
                x, y = self.map_position(tile.x_axis, tile.y_axis)
                self.create_image(x, y, image=self.normal_tile, tag=f"normal_tile_{index}_{tile_index}", anchor=NW)
                if state == False:
                    self.itemconfig(f"normal_tile_{index}_{tile_index}", state="hidden")

        x, y = self.block.first_block.get_position()
        x, y = self.map_position(x, y)
        self.first_block_id = self.create_image(x, y, image=self.single_block, tag="singe_block_1", anchor=NW)

        x, y = self.block.first_block.get_position()
        x, y = self.map_position(x, y)
        self.second_block_id = self.create_image(x, y, image=self.single_block, tag="singe_block_1", anchor=NW)

    def rerender_bridges(self):
        for (index, state) in enumerate(self.list_state):
            for tile_index in range(0, len(self.game_board.bridges[index].list_tile)):
                if state == False:
                    print(f"normal_tile_{index}_{tile_index}")
                    self.itemconfig(f"normal_tile_{index}_{tile_index}", state="hidden")
                else:
                    self.itemconfig(f"normal_tile_{index}_{tile_index}", state="normal")

    def auto_play(self, result):
        action = result.pop(0)
        if action == "TURN_UP":
            self.block.move_up()
        elif action == "TURN_DOWN":
            self.block.move_down()
        elif action == "TURN_LEFT":
            self.block.move_left()
        elif action == "TURN_RIGHT":
            self.block.move_right()
        elif action == "TOGGLE_FOCUSSING":
            self.block.toggle_focussing()
        # trigger the switch if it is possible
        tiles = []
        x_1, y_1 = self.block.first_block.get_position()
        x_2, y_2 = self.block.second_block.get_position()
        tile_1 = self.game_board.map[x_1][y_1]
        tile_2 = self.game_board.map[x_2][y_2]
        tiles.append(tile_1)
        if tile_2 != tile_1:
            tiles.append(tile_2)
        for tile in tiles:
            if isinstance(tile, TeleportSwitch):
                tile.trigger(self.block)
            elif isinstance(tile, NormalSwitch):
                tile.trigger(self.block, self.list_state)
                self.game_board.update_map(self.list_state)
                self.rerender_bridges()

        x_1, y_1 = self.block.first_block.get_position()
        x_1, y_1 = self.map_position(x_1, y_1)
        x_2, y_2 = self.block.second_block.get_position()
        x_2, y_2 = self.map_position(x_2, y_2)
        self.moveto(self.first_block_id, x_1, y_1)
        self.moveto(self.second_block_id, x_2, y_2)

        if len(result) > 0:
            self.after(1000, lambda: self.auto_play(result))

    def map_position(self, x, y):
        _x = x * BloxorzBoard.TILE_SIZE + self.pad_x
        _y = (self.game_board.height - y - 1) * BloxorzBoard.TILE_SIZE + self.pad_y
        return _x, _y
