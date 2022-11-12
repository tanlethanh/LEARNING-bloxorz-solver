from tkinter import Tk, Label, Button, NW, Canvas

from PIL import Image
from PIL.ImageTk import PhotoImage

from bloxorz.bloxorz_solver import BloxorzSolver
from bloxorz.element.block import DoubleBlock
from bloxorz.gui.bloxorz_board import BloxorzBoard
from bloxorz.gui.bloxorz_control_panel import BloxorzControlPanel


def solve_button_onclick(control_panel, bloxorz_board: BloxorzBoard):

    input_filename = f"input{control_panel.get_stage()}.JSON"
    game_board, state_bridges, initial_position = BloxorzSolver.parse_input_data(input_filename)
    block = DoubleBlock(initial_position)
    bloxorz_board.reset_game(game_board=game_board, block=block, list_state=state_bridges)

    if control_panel.get_algorithm() in ["DFS", "BFS"]:
        solution = BloxorzSolver.blind_solve(input_filename, control_panel.get_algorithm())
        bloxorz_board.render_blind_statistic(solution["report"])
    else:
        print(control_panel.get_population_size())
        print(control_panel.get_chromosome_length())
        print(control_panel.get_mutation_chane())
        print(control_panel.get_distance_type())
        print(control_panel.get_cross_type())
        solution = BloxorzSolver.genetic_solve(input_filename,
                                               control_panel.get_population_size(),
                                               control_panel.get_chromosome_length(),
                                               control_panel.get_mutation_chane(),
                                               control_panel.get_cross_type(),
                                               control_panel.get_distance_type()
                                               )
        bloxorz_board.render_genetic_statistic(solution["report"])

    bloxorz_board.auto_play(solution["solution"])


if __name__ == '__main__':
    root = Tk(screenName="Bloxorz game", className="bloxorz")
    root.geometry("1100x600")
    background_image = PhotoImage(Image.open("bloxorz/gui/images/background.jpg").resize(size=(1100, 600)))
    background = Label(root, image=background_image)
    background.place(x=0, y=0, relwidth=1, relheight=1)

    bloxorz_control_panel = BloxorzControlPanel(master=root)
    bloxorz_control_panel.pack()

    solve_button_image = PhotoImage(file="bloxorz/gui/images/solve_button.png")
    bloxorz_game = BloxorzBoard(root)
    solve_button = Button(image=solve_button_image,
                          borderwidth=0,
                          highlightthickness=0,
                          command=lambda: solve_button_onclick(bloxorz_control_panel, bloxorz_game),
                          relief="flat")

    solve_button.place(x=880, y=20)

    root.resizable(False, False)
    root.mainloop()
