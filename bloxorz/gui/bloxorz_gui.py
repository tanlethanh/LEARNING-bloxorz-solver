import json
import os.path
import subprocess
import sys
import time
import tkinter
from tkinter import Tk, Frame, Canvas, ALL, NW, OptionMenu, StringVar, Radiobutton, Button
from PIL import Image, ImageTk

from bloxorz.block import DoubleBlock
from bloxorz.game_board import GameBoard
from bloxorz.switch import NormalSwitch, TeleportSwitch
from bloxorz.tile import TileType
from bloxorz.bloxorz_solver import BloxorzSolver


class BloxorzBoard(Canvas):
    TILE_SIZE = 40

    def __init__(self, master, game_board: GameBoard, block: DoubleBlock, list_state):

        self.game_board = game_board
        self.block = block
        self.list_state = list_state
        super().__init__(master=master, width=game_board.width * BloxorzBoard.TILE_SIZE,
                         height=game_board.height * BloxorzBoard.TILE_SIZE, borderwidth=0, highlightthickness=0)

        self.init_game()

    def init_game(self):

        self.load_images()
        self.create_objects()
        # self.locateApple()
        # self.bind_all("<Key>", self.onKeyPressed)
        # self.after(Cons.DELAY, self.onTimer)

    def load_images(self):
        try:
            self.i_normal_tile = Image.open("images/normal-tile.png") \
                .resize(size=(BloxorzBoard.TILE_SIZE, BloxorzBoard.TILE_SIZE))
            self.normal_tile = ImageTk.PhotoImage(self.i_normal_tile)

            self.i_orange_tile = Image.open("images/orange-tile.png") \
                .resize(size=(BloxorzBoard.TILE_SIZE, BloxorzBoard.TILE_SIZE))
            self.orange_tile = ImageTk.PhotoImage(self.i_orange_tile)

            self.i_normal_switch = Image.open("images/normal-sw.png") \
                .resize(size=(BloxorzBoard.TILE_SIZE, BloxorzBoard.TILE_SIZE))
            self.normal_switch = ImageTk.PhotoImage(self.i_normal_switch)

            self.i_single_block = Image.open("images/single-block.png") \
                .resize(size=(BloxorzBoard.TILE_SIZE, BloxorzBoard.TILE_SIZE))
            self.single_block = ImageTk.PhotoImage(self.i_single_block)


        except IOError as e:
            print(e)
            sys.exit(1)

    def create_objects(self):
        for col in self.game_board.map:
            for ele in col:
                if isinstance(ele, NormalSwitch):
                    self.create_image(ele.x_axis * BloxorzBoard.TILE_SIZE,
                                      (self.game_board.height - ele.y_axis - 1) * BloxorzBoard.TILE_SIZE,
                                      image=self.normal_switch,
                                      tag="normal_switch",
                                      anchor=NW)
                elif ele.state == TileType.ON:
                    self.create_image(ele.x_axis * BloxorzBoard.TILE_SIZE,
                                      (self.game_board.height - ele.y_axis - 1) * BloxorzBoard.TILE_SIZE,
                                      image=self.normal_tile,
                                      tag="normal_tile",
                                      anchor=NW)
                elif ele.state == TileType.ORANGE:
                    self.create_image(ele.x_axis * BloxorzBoard.TILE_SIZE,
                                      (self.game_board.height - ele.y_axis - 1) * BloxorzBoard.TILE_SIZE,
                                      image=self.orange_tile,
                                      tag="orange_tile",
                                      anchor=NW)

        for (index, state) in enumerate(self.list_state):
            for (tile_index, tile) in enumerate(self.game_board.bridges[state].list_tile):
                self.create_image(tile.x_axis * BloxorzBoard.TILE_SIZE,
                                  (self.game_board.height - tile.y_axis - 1) * BloxorzBoard.TILE_SIZE,
                                  image=self.normal_tile,
                                  tag=f"normal_tile_{index}_{tile_index}",
                                  anchor=NW)
                if state == False:
                    self.itemconfig(f"normal_tile_{index}_{tile_index}", state="hidden")

        x_1, y_1 = self.block.first_block.get_position()
        self.first_block_id = self.create_image(x_1 * BloxorzBoard.TILE_SIZE,
                                                (self.game_board.height - y_1 - 1) * BloxorzBoard.TILE_SIZE,
                                                image=self.single_block,
                                                tag="singe_block_1",
                                                anchor=NW
                                                )
        x_2, y_2 = self.block.second_block.get_position()
        self.second_block_id = self.create_image(x_2 * BloxorzBoard.TILE_SIZE,
                                                 (self.game_board.height - y_2 - 1) * BloxorzBoard.TILE_SIZE,
                                                 image=self.single_block,
                                                 tag="singe_block_2",
                                                 anchor=NW)

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
        x_2, y_2 = self.block.second_block.get_position()
        self.moveto(self.first_block_id, x_1 * BloxorzBoard.TILE_SIZE,
                    (self.game_board.height - y_1 - 1) * BloxorzBoard.TILE_SIZE)
        self.moveto(self.second_block_id, x_2 * BloxorzBoard.TILE_SIZE,
                    (self.game_board.height - y_2 - 1) * BloxorzBoard.TILE_SIZE)

        if len(result) > 0:
            self.after(1000, lambda: self.auto_play(result))


def algorithm_onchange(algorithm, genetic_paras):
    alg = algorithm.get()
    if alg == "Genetic":
        genetic_paras.grid(row=1, column=0, columnspan=6, sticky="w")
    elif alg == "DFS" or alg == "BFS":
        genetic_paras.grid_forget()


def solve_button_onclick(**kwargs):
    result = BloxorzSolver.blind_solve(kwargs["file_name"], kwargs["algorithm"])
    kwargs["result"].set(result)
    print(kwargs["result"].get())


def render_solving(root: tkinter.Misc, result, input_file_name):
    with open(input_file_name) as f:
        input_data = json.load(f)

    # Create bloxorz game board and initial position
    game_board = GameBoard(input_data["map"], input_data["bridges"])
    initial_position = input_data["initial_position"]
    initial_position = initial_position.split(" ")
    initial_position = tuple(int(pos) for pos in initial_position)

    try:
        state_bridges = input_data["state_bridges"]
        state_bridges = [bool(state) for state in state_bridges]
    except Exception as e:
        print(e)
        state_bridges = [False] * len(game_board.bridges)

    block = DoubleBlock(initial_position)

    bloxorz_board = BloxorzBoard(master=root, game_board=game_board, block=block, list_state=state_bridges)
    bloxorz_board.grid(row=2, column=0, columnspan=10, sticky="w", padx=300)
    bloxorz_board.auto_play(result)


def main():
    root = Tk(screenName="Bloxorz game", className="bloxorz")
    # root.attributes("-fullscreen", True)
    root.geometry("1100x600")
    background_image = ImageTk.PhotoImage(Image.open("./images/background.jpg").resize(size=(1100, 600)))
    background = tkinter.Label(root, image=background_image)
    background.place(x=0, y=0, relwidth=1, relheight=1)

    root.rowconfigure(2, weight=1)

    MINI_HEIGHT = 50

    # menu = tkinter.Label(root, background="gray")
    # menu.grid(row=0, column=0, columnspan=4, rowspan=1)

    # stage frame
    stage_frame = Frame(master=root, bg='white', height=MINI_HEIGHT)
    # stage_frame.rowconfigure(0, weight=1)
    stage_title = tkinter.Label(master=stage_frame, text="Stage: ")
    stage_title.grid(row=0, column=1)
    stage_number = StringVar()
    stage_number.set("01")
    stage_option = OptionMenu(stage_frame, stage_number, "01", "02", "03", "04", "05", "10", "33")
    stage_option.grid(row=0, column=2)

    # algorithm frame
    algorithm_frame = Frame(master=root, bg='white', height=MINI_HEIGHT)
    algorithm_title = tkinter.Label(master=algorithm_frame, text="Algorithm: ")
    algorithm = StringVar()
    algorithm.set("none")
    R1 = Radiobutton(algorithm_frame, text="DFS", value="DFS", variable=algorithm)
    R2 = Radiobutton(algorithm_frame, text="BrFS", value="BFS", variable=algorithm)
    R3 = Radiobutton(algorithm_frame, text="Genetic", value="Genetic", variable=algorithm)
    algorithm_title.grid(row=0, column=0)
    R1.grid(row=0, column=1)
    R2.grid(row=0, column=2)
    R3.grid(row=0, column=3)

    # genetic para
    population_size = tkinter.Variable()
    chromosome_length = tkinter.Variable()
    mutation_chance = tkinter.Variable()

    genetic_paras = Frame(master=root, bg='white', height=MINI_HEIGHT)
    population_size_label = tkinter.Label(master=genetic_paras, text="Population size: ")
    chromosome_length_label = tkinter.Label(master=genetic_paras, text="Chromosome length: ")
    mutation_chance_label = tkinter.Label(master=genetic_paras, text="Mutation chance: ")
    population_size_entry = tkinter.Entry(master=genetic_paras, textvariable=population_size)
    chromosome_length_entry = tkinter.Entry(master=genetic_paras, textvariable=chromosome_length)
    mutation_chance_entry = tkinter.Entry(master=genetic_paras, textvariable=mutation_chance)
    population_size_label.grid(row=0, column=0)
    population_size_entry.grid(row=0, column=1)
    chromosome_length_label.grid(row=0, column=2)
    chromosome_length_entry.grid(row=0, column=3)
    mutation_chance_label.grid(row=0, column=4)
    mutation_chance_entry.grid(row=0, column=5)

    # algorithm.trace(mode='w', )
    algorithm.trace('w', lambda s1, s2, s3: algorithm_onchange(algorithm, genetic_paras))

    result = tkinter.Variable()
    solve_button = Button(master=root, text="Solve",
                          command=lambda: solve_button_onclick(
                              file_name=f"../../input/input{str(int(stage_number.get()))}.JSON",
                              algorithm=algorithm.get(),
                              population_size=population_size,
                              chromosome_length=chromosome_length,
                              mutation_chance=mutation_chance,
                              result=result
                          ))

    result.trace("w", lambda s1, s2, s3: render_solving(root, list(result.get()),
                                                        f"../../input/input{str(int(stage_number.get()))}.JSON"))

    # set main layout
    stage_frame.grid(row=0, column=0, columnspan=2)
    algorithm_frame.grid(row=0, column=2, columnspan=3)
    solve_button.grid(row=0, column=6)

    root.mainloop()


if __name__ == '__main__':
    main()
