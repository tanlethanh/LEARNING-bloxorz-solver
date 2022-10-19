from enum import Enum


def manhattan_distance(f, s):
    if isinstance(f, SingleBlock) and isinstance(s, SingleBlock):
        return abs(f.x_axis - s.x_axis) + abs(f.y_axis - s.y_axis)
    elif isinstance(f, tuple) and isinstance(s, tuple):
        return abs(f[0] - s[0]) + abs(f[1] - s[1])


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
        match self.state:
            case DoubleBlockState.STANDING:
                self.first_block.move_up(step=2)
                self.second_block.move_up(step=1)

            case DoubleBlockState.LYING:
                self.first_block.move_up(step=1)
                self.second_block.move_up(step=1)

            case DoubleBlockState.DIVIDED:
                if not isinstance(self.focussing, SingleBlock):
                    raise Exception(f"Focussing block must be SingleBlock when {self} is DIVIDED")
                self.focussing.move_up(step=1)
                if manhattan_distance(self.first_block, self.second_block) == 1:
                    self.state = DoubleBlockState.LYING
                    self.focussing = None

    def move_down(self):
        match self.state:
            case DoubleBlockState.STANDING:
                self.first_block.move_down(step=2)
                self.second_block.move_down(step=1)

            case DoubleBlockState.LYING:
                self.first_block.move_down(step=1)
                self.second_block.move_down(step=1)

            case DoubleBlockState.DIVIDED:
                if not isinstance(self.focussing, SingleBlock):
                    raise Exception(f"Focussing block must be SingleBlock when {self} is DIVIDED")
                self.focussing.move_down(step=1)
                if manhattan_distance(self.first_block, self.second_block) == 1:
                    self.state = DoubleBlockState.LYING
                    self.focussing = None

    def move_left(self):
        match self.state:
            case DoubleBlockState.STANDING:
                self.first_block.move_left(step=2)
                self.second_block.move_left(step=1)

            case DoubleBlockState.LYING:
                self.first_block.move_left(step=1)
                self.second_block.move_left(step=1)

            case DoubleBlockState.DIVIDED:
                if not isinstance(self.focussing, SingleBlock):
                    raise Exception(f"Focussing block must be SingleBlock when {self} is DIVIDED")
                self.focussing.move_left(step=1)
                if manhattan_distance(self.first_block, self.second_block) == 1:
                    self.state = DoubleBlockState.LYING
                    self.focussing = None

    def move_right(self):
        match self.state:
            case DoubleBlockState.STANDING:
                self.first_block.move_right(step=2)
                self.second_block.move_right(step=1)

            case DoubleBlockState.LYING:
                self.first_block.move_right(step=1)
                self.second_block.move_right(step=1)

            case DoubleBlockState.DIVIDED:
                if not isinstance(self.focussing, SingleBlock):
                    raise Exception(f"Focussing block must be SingleBlock when {self} is DIVIDED")
                self.focussing.move_right(step=1)
                if manhattan_distance(self.first_block, self.second_block) == 1:
                    self.state = DoubleBlockState.LYING
                    self.focussing = None

    def toggle_focussing(self):
        if self.state == DoubleBlockState.DIVIDED:
            if self.first_block.equals(self.focussing):
                self.focussing = self.first_block
            elif self.second_block.equals(self.focussing):
                self.focussing = self.second_block
            else:
                raise Exception(f"Cannot toggle focussing for {self}, focussing block is invalid")
        else:
            raise Exception(f"Cannot toggle focussing for {self}, the state must be DIVIDED")

    def equals(self, block):
        if not isinstance(block, DoubleBlock):
            return False
        return (
            self.focussing == self.focussing
            and self.state == block.state
            and
            (
                (self.first_block.equals(block.first_block) and self.second_block.equals(block.second_block))
                or
                (self.first_block.equals(block.second_block) and self.second_block.equals(block.first_block))
            )
        )


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

    def move_up(self, step):
        if isinstance(step, int):
            self.y_axis += step

    def move_down(self, step):
        if isinstance(step, int):
            self.y_axis -= step

    def move_left(self, step):
        if isinstance(step, int):
            self.x_axis -= step

    def move_right(self, step):
        if isinstance(step, int):
            self.x_axis += step

    def equals(self, block):
        return self.x_axis == block.x_axis and self.y_axis == block.y_axis
