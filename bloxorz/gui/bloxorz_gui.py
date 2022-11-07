import json
import sys
import tkinter
from tkinter import Tk, Frame, Canvas, NW, OptionMenu, StringVar, Radiobutton, Button
from PIL import Image, ImageTk

from bloxorz.element.block import DoubleBlock
from bloxorz.element.game_board import GameBoard
from bloxorz.bloxorz_solver import BloxorzSolver
from bloxorz.gui.bloxorz_board import BloxorzBoard


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
    bloxorz_board.auto_play(result["solution"])


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
                              file_name=f"input{str(int(stage_number.get()))}.JSON",
                              algorithm=algorithm.get(),
                              population_size=population_size,
                              chromosome_length=chromosome_length,
                              mutation_chance=mutation_chance
                          ))

    # set main layout
    stage_frame.grid(row=0, column=0, columnspan=2)
    algorithm_frame.grid(row=0, column=2, columnspan=3)
    solve_button.grid(row=0, column=6)

    root.mainloop()


if __name__ == '__main__':
    main()
