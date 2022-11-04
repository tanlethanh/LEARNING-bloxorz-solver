import json
import sys
from tkinter import Tk, Frame, Canvas, ALL, NW
from PIL import Image, ImageTk
from bloxorz.game_board import GameBoard


class BloxorzBoard(Canvas):

    TILE_SIZE = 40

    def __init__(self, game_board: GameBoard):
        super().__init__(width=game_board.width * BloxorzBoard.TILE_SIZE,
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
        self.create_text(1 * BloxorzBoard.TILE_SIZE, 1 * BloxorzBoard.TILE_SIZE, fill="white", text="Hello Bloxorz")
        self.create_image(1 * BloxorzBoard.TILE_SIZE, 3 * BloxorzBoard.TILE_SIZE, image=self.normal_tile, tag="normal_tile")
        self.create_image(6 * BloxorzBoard.TILE_SIZE, 3 * BloxorzBoard.TILE_SIZE, image=self.normal_tile, tag="normal_tile")
        self.create_image(4 * BloxorzBoard.TILE_SIZE, 3 * BloxorzBoard.TILE_SIZE, image=self.normal_tile, tag="normal_tile")
        self.create_image(4 * BloxorzBoard.TILE_SIZE, 5 * BloxorzBoard.TILE_SIZE, image=self.normal_tile, tag="normal_tile")

    # def checkAppleCollision(self):
    #     '''checks if the head of snake collides with apple'''
    #
    #     apple = self.find_withtag("apple")
    #     head = self.find_withtag("head")
    #
    #     x1, y1, x2, y2 = self.bbox(head)
    #     overlap = self.find_overlapping(x1, y1, x2, y2)
    #
    #     for ovr in overlap:
    #
    #         if apple[0] == ovr:
    #
    #             self.score += 1
    #             x, y = self.coords(apple)
    #             self.create_image(x, y, image=self.dot, anchor=NW, tag="dot")
    #             self.locateApple()


    # def moveSnake(self):
    #     '''moves the Snake object'''
    #
    #     dots = self.find_withtag("dot")
    #     head = self.find_withtag("head")
    #
    #     items = dots + head
    #
    #     z = 0
    #     while z < len(items)-1:
    #
    #         c1 = self.coords(items[z])
    #         c2 = self.coords(items[z+1])
    #         self.move(items[z], c2[0]-c1[0], c2[1]-c1[1])
    #         z += 1
    #
    #     self.move(head, self.moveX, self.moveY)


    # def checkCollisions(self):
    #     '''checks for collisions'''
    #
    #     dots = self.find_withtag("dot")
    #     head = self.find_withtag("head")
    #
    #     x1, y1, x2, y2 = self.bbox(head)
    #     overlap = self.find_overlapping(x1, y1, x2, y2)
    #
    #     for dot in dots:
    #         for over in overlap:
    #             if over == dot:
    #               self.inGame = False
    #
    #     if x1 < 0:
    #         self.inGame = False
    #
    #     if x1 > Cons.BOARD_WIDTH - Cons.DOT_SIZE:
    #         self.inGame = False
    #
    #     if y1 < 0:
    #         self.inGame = False
    #
    #     if y1 > Cons.BOARD_HEIGHT - Cons.DOT_SIZE:
    #         self.inGame = False


    # def locateApple(self):
    #     '''places the apple object on Canvas'''
    #
    #     apple = self.find_withtag("apple")
    #     self.delete(apple[0])
    #
    #     r = random.randint(0, Cons.MAX_RAND_POS)
    #     self.appleX = r * Cons.DOT_SIZE
    #     r = random.randint(0, Cons.MAX_RAND_POS)
    #     self.appleY = r * Cons.DOT_SIZE
    #
    #     self.create_image(self.appleX, self.appleY, anchor=NW,
    #         image=self.apple, tag="apple")


    # def onKeyPressed(self, e):
    #     '''controls direction variables with cursor keys'''
    #
    #     key = e.keysym
    #
    #     LEFT_CURSOR_KEY = "Left"
    #     if key == LEFT_CURSOR_KEY and self.moveX <= 0:
    #
    #         self.moveX = -Cons.DOT_SIZE
    #         self.moveY = 0
    #
    #     RIGHT_CURSOR_KEY = "Right"
    #     if key == RIGHT_CURSOR_KEY and self.moveX >= 0:
    #
    #         self.moveX = Cons.DOT_SIZE
    #         self.moveY = 0
    #
    #     RIGHT_CURSOR_KEY = "Up"
    #     if key == RIGHT_CURSOR_KEY and self.moveY <= 0:
    #
    #         self.moveX = 0
    #         self.moveY = -Cons.DOT_SIZE
    #
    #     DOWN_CURSOR_KEY = "Down"
    #     if key == DOWN_CURSOR_KEY and self.moveY >= 0:
    #
    #         self.moveX = 0
    #         self.moveY = Cons.DOT_SIZE


    # def onTimer(self):
    #     '''creates a game cycle each timer event'''
    #
    #     self.drawScore()
    #     self.checkCollisions()
    #
    #     if self.inGame:
    #         self.checkAppleCollision()
    #         self.moveSnake()
    #         self.after(Cons.DELAY, self.onTimer)
    #     else:
    #         self.gameOver()


    # def drawScore(self):
    #     '''draws score'''
    #
    #     score = self.find_withtag("score")
    #     self.itemconfigure(score, text="Score: {0}".format(self.score))


    # def gameOver(self):
    #     '''deletes all objects and draws game over message'''
    #
    #     self.delete(ALL)
    #     self.create_text(self.winfo_width() /2, self.winfo_height()/2,
    #         text="Game Over with score {0}".format(self.score), fill="white")


# class Snake(Frame):
#
#     def __init__(self):
#         super().__init__()
#
#         self.master.title('Snake')
#         self.board = Board()
#         self.pack()


def main():

    root = Tk(screenName="Bloxorz game", className="bloxorz")
    root.size()

    root.geometry("1000x1000")

    file_name = "../../input/input1.JSON"
    with open(file_name) as f:
        input_data = json.load(f)

    # Create bloxorz game board and initial position
    game_board = GameBoard(input_data["map"], input_data["bridges"])
    # initial_position = input_data["initial_position"]
    # initial_position = initial_position.split(" ")
    # initial_position = tuple(int(pos) for pos in initial_position)

    bloxorz_board = BloxorzBoard(game_board)
    bloxorz_board.pack()
    root.mainloop()


if __name__ == '__main__':
    main()
