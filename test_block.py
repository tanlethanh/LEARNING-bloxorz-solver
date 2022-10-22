# print([e for e in Action])
# test single block
# sg_block = SingleBlock(1, 2)
# print(sg_block)
# sg_block.move_up()
# print(sg_block)
# sg_block.move_down()
# print(sg_block)
# sg_block.move_left()
# print(sg_block)
# sg_block.move_right()
# print(sg_block)
import random

from bloxorz.block import DoubleBlockState, DoubleBlock

#test double block

# col -> row
db_block = DoubleBlock((0, 0))
print(db_block.first_block)
print(db_block.second_block)
def test_move_db_block():
    for i in range(1, 20):
        a = random.randint(1, 4)
        if a == 1:
            db_block.move_up()
            print("move up")
        elif a == 2:
            db_block.move_down()
            print("move down")
        elif a == 3:
            db_block.move_left()
            print("move left")
        else:
            db_block.move_right()
            print("move right")

        maps = [["-" for i in range(1, 10)] for j in range(1, 10)]

        try:
            if (
                db_block.first_block.x_axis < 0
                or db_block.second_block.x_axis < 0
                or db_block.first_block.y_axis < 0
                or db_block.second_block.y_axis < 0
            ):
                raise Exception("Index is negative")
            maps[db_block.first_block.x_axis][db_block.first_block.y_axis] = "*"
            maps[db_block.second_block.x_axis][db_block.second_block.y_axis] = "*"
        except Exception as e:
            print(e)
            db_block.first_block.set_position(0, 0)
            db_block.second_block.set_position(0, 0)
            db_block.state = DoubleBlockState.STANDING
            continue

        rows, cols = len(maps), len(maps[0])
        for y in range(0, cols).__reversed__():
            for x in range(0, rows):
                print(maps[x][y], end="")
            print("")

test_move_db_block()
