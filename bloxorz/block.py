from enum import Enum


def manhattan_distance(f_pos, s_pos):
    return abs(f_pos[0] - s_pos[0]) + abs(f_pos[1] - s_pos[1])


class DoubleBlockState(Enum):
    STANDING = 1
    LYING = 2
    DIVIDED = 0


class DoubleBlock:

    def __init__(self, **kwargs):
        if kwargs["block"] is not None and isinstance(kwargs["block"], DoubleBlock):
            self.first_block = SingleBlock(block=kwargs["block"].first_block)
            self.second_block = SingleBlock(block=kwargs["block"].second_block)
            self.state = kwargs["block"].state
            self.focussing = kwargs["block"].state

        elif kwargs["initial_position"] is not None and isinstance(kwargs["initial_position"], DoubleBlock):
            self.first_block = SingleBlock(x_axis=kwargs["initial_position"][0], y_axis=kwargs["initial_position"][1])
            self.second_block = SingleBlock(block=self.first_block)
            self.state = DoubleBlockState.STANDING
            self.focussing = None

        else:
            raise Exception("Some fields are invalid to initialize a double block")

    def move_up(self):
        pass

    def move_down(self):
        pass

    def move_left(self):
        pass

    def move_right(self):
        pass

    def equals(self, block):
        if not isinstance(block, DoubleBlock):
            return False
        return (
            self.first_block.equals(block.first_block)
            and self.second_block.equals(block.second_block)
            and self.focussing == self.focussing
            and self.state == block.state
        )

    def toggle_focussing(self):
        if self.first_block.equals(self.focussing):
            self.focussing = self.first_block
        elif self.second_block.equals(self.focussing):
            self.focussing = self.second_block
        else:
            raise Exception(f"Cannot toggle focussing for {self}")


class SingleBlock:

    def __init__(self, **kwargs):
        if kwargs["block"] is not None and isinstance(kwargs["block"], SingleBlock):
            self.x_axis = kwargs["block"].x_axis
            self.y_axis = kwargs["block"].y_axis
        elif kwargs["x_axis"] is not None and kwargs["y_axis"] is not None:
            self.x_axis = int(kwargs["x_axis"])
            self.y_axis = int(kwargs["y_axis"])
        else:
            raise Exception("Some fields are invalid to initialize a single block")

    def set_position(self, x_axis, y_axis):
        self.x_axis = x_axis
        self.y_axis = y_axis

    def move_up(self):
        pass

    def move_down(self):
        pass

    def move_left(self):
        pass

    def move_right(self):
        pass

    def equals(self, block):
        return self.x_axis == block.x_axis and self.y_axis == block.y_axis
