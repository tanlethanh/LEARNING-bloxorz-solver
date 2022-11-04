import json
import sys
import tkinter
from tkinter import Tk, Frame, Canvas, ALL, NW, OptionMenu, StringVar, Radiobutton
from PIL import Image, ImageTk
from bloxorz.game_board import GameBoard
from bloxorz.tile import TileType


class BloxorzBoard(Canvas):

    TILE_SIZE = 40

    def __init__(self, master, game_board: GameBoard):

        self.game_board = game_board
        super().__init__(master=master, width=game_board.width * BloxorzBoard.TILE_SIZE,
                         height=game_board.height * BloxorzBoard.TILE_SIZE,
                         background="orange", borderwidth=0, highlightthickness=0)
        self.init_game()
        self.pack()

    def init_game(self):

        self.load_images()
        self.create_objects()
        # self.locateApple()
        # self.bind_all("<Key>", self.onKeyPressed)
        # self.after(Cons.DELAY, self.onTimer)

    def load_images(self):
        try:
            self.i_normal_tile = Image.open("./images/normal-tile.png")\
                .resize(size=(BloxorzBoard.TILE_SIZE, BloxorzBoard.TILE_SIZE))
            self.normal_tile = ImageTk.PhotoImage(self.i_normal_tile)
            self.i_orange_tile = Image.open("./images/orange-tile.png")\
                .resize(size=(BloxorzBoard.TILE_SIZE, BloxorzBoard.TILE_SIZE))
            self.orange_tile = ImageTk.PhotoImage(self.i_orange_tile)
        except IOError as e:
            print(e)
            sys.exit(1)

    def create_objects(self):
        for col in self.game_board.map:
            for ele in col:
                if ele.state == TileType.ON:
                    self.create_image(ele.x_axis * BloxorzBoard.TILE_SIZE,
                                      (self.game_board.height - ele.y_axis - 1) * BloxorzBoard.TILE_SIZE,
                                      image=self.normal_tile,
                                      tag="normal_tile",
                                      anchor=NW)


def algorithm_onchange(algorithm, genetic_paras):
    alg = algorithm.get()
    if alg == "Genetic":
        genetic_paras.grid(row=4)
    elif alg == "DFS" or alg == "BFS":
        genetic_paras.grid_forget()


def main():
    root = Tk(screenName="Bloxorz game", className="bloxorz")
    root.geometry("1000x1000")

    file_name = "../../input/input1.JSON"
    with open(file_name) as f:
        input_data = json.load(f)

    # Create bloxorz game board and initial position
    game_board = GameBoard(input_data["map"], input_data["bridges"])
    bloxorz_board = BloxorzBoard(master=root, game_board=game_board)
    bloxorz_board.grid(row=0)


    # stage frame
    stage_frame = Frame(master=root, bg='cyan', width=450, height=50, pady=3)
    stage_frame.grid(row=1)
    stage_title = tkinter.Label(master=stage_frame, text="Stage: ")
    stage_title.grid(row=0, column=1)
    stage_number = StringVar(master=root)
    stage_number.set("01")
    stage_option = OptionMenu(stage_frame, stage_number, "01", "02", "03", "04", "05", "10", "33")
    stage_option.grid(row=0, column=2)

    # algorithm frame
    algorithm_frame = Frame(master=root, bg='gray', width=450, height=50, pady=3)
    algorithm_frame.grid(row=3)
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
    population_size = ""
    chromosome_length = ""
    genetic_paras = Frame(master=root, bg='red', width=450, height=50, pady=3)
    population_size_label = tkinter.Label(master=genetic_paras, text="Population size: ")
    chromosome_length_label = tkinter.Label(master=genetic_paras, text="Chromosome length: ")
    population_size_entry = tkinter.Entry(master=genetic_paras, textvariable=population_size)
    chromosome_length_entry = tkinter.Entry(master=genetic_paras, textvariable=chromosome_length)
    population_size_label.grid(row=0, column=0)
    population_size_entry.grid(row=0, column=1)
    chromosome_length_label.grid(row=0, column=2)
    chromosome_length_entry.grid(row=0, column=3)

    # algorithm.trace(mode='w', )
    algorithm.trace('w', lambda s1, s2, s3: algorithm_onchange(algorithm, genetic_paras))
    root.mainloop()




if __name__ == '__main__':
    main()







