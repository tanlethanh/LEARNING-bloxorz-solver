from enum import Enum

from multipledispatch import dispatch


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

    @dispatch(tuple)
    def __init__(self, position):
        self.first_block = SingleBlock(position[0], position[1])
        self.second_block = SingleBlock(self.first_block)
        self.state = DoubleBlockState.STANDING
        self.focussing = None

    @dispatch(object)
    def __init__(self, block):
        if block is not None and isinstance(block, DoubleBlock):
            self.first_block = SingleBlock(block.first_block)
            self.second_block = SingleBlock(block.second_block)
            self.state = block.state
            if block.state == DoubleBlockState.DIVIDED:
                if block.focussing == block.first_block:
                    self.focussing = self.first_block
                elif block.focussing == block.second_block:
                    self.focussing = self.second_block
            else:
                self.focussing = None
        else:
            raise Exception("Some fields are invalid to initialize a double block")

    def __eq__(self, block) -> bool:
        if not isinstance(block, DoubleBlock):
            return False
        return (
                self.focussing == block.focussing
                and self.state == block.state
                and
                (
                        (self.first_block == block.first_block and self.second_block == block.second_block)
                        or
                        (self.first_block == block.second_block and self.second_block == block.first_block)
                )
        )

    def __str__(self) -> str:
        return f"DB {self.state.name} f: {self.first_block} s: {self.second_block}"

    def move_up(self):
        match self.state:
            case DoubleBlockState.STANDING:
                self.first_block.move_up(step=2)
                self.second_block.move_up(step=1)
                self.state = DoubleBlockState.LYING

            case DoubleBlockState.LYING:
                if self.first_block.y_axis == self.second_block.y_axis:
                    self.first_block.move_up(step=1)
                    self.second_block.move_up(step=1)
                elif self.first_block.y_axis > self.second_block.y_axis:
                    self.first_block.move_up(step=1)
                    self.second_block.move_up(step=2)
                    self.state = DoubleBlockState.STANDING
                else:
                    self.first_block.move_up(step=2)
                    self.second_block.move_up(step=1)
                    self.state = DoubleBlockState.STANDING

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
                self.state = DoubleBlockState.LYING

            case DoubleBlockState.LYING:
                if self.first_block.y_axis == self.second_block.y_axis:
                    self.first_block.move_down(step=1)
                    self.second_block.move_down(step=1)
                elif self.first_block.y_axis > self.second_block.y_axis:
                    self.first_block.move_down(step=2)
                    self.second_block.move_down(step=1)
                    self.state = DoubleBlockState.STANDING
                else:
                    self.first_block.move_down(step=1)
                    self.second_block.move_down(step=2)
                    self.state = DoubleBlockState.STANDING

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
                self.state = DoubleBlockState.LYING

            case DoubleBlockState.LYING:
                if self.first_block.x_axis == self.second_block.x_axis:
                    self.first_block.move_left(step=1)
                    self.second_block.move_left(step=1)
                elif self.first_block.x_axis > self.second_block.x_axis:
                    self.first_block.move_left(step=2)
                    self.second_block.move_left(step=1)
                    self.state = DoubleBlockState.STANDING
                else:
                    self.first_block.move_left(step=1)
                    self.second_block.move_left(step=2)
                    self.state = DoubleBlockState.STANDING

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
                self.state = DoubleBlockState.LYING

            case DoubleBlockState.LYING:
                if self.first_block.x_axis == self.second_block.x_axis:
                    self.first_block.move_right(step=1)
                    self.second_block.move_right(step=1)
                elif self.first_block.x_axis > self.second_block.x_axis:
                    self.first_block.move_right(step=1)
                    self.second_block.move_right(step=2)
                    self.state = DoubleBlockState.STANDING
                else:
                    self.first_block.move_right(step=2)
                    self.second_block.move_right(step=1)
                    self.state = DoubleBlockState.STANDING

            case DoubleBlockState.DIVIDED:
                if not isinstance(self.focussing, SingleBlock):
                    raise Exception(f"Focussing block must be SingleBlock when {self} is DIVIDED")
                self.focussing.move_right(step=1)
                if manhattan_distance(self.first_block, self.second_block) == 1:
                    self.state = DoubleBlockState.LYING
                    self.focussing = None

    def toggle_focussing(self):
        if self.state == DoubleBlockState.DIVIDED:
            if self.first_block == self.focussing:
                self.focussing = self.second_block
            elif self.second_block == self.focussing:
                self.focussing = self.first_block
            else:
                raise Exception(f"Cannot toggle focussing for {self}, focussing block is invalid")
        else:
            raise Exception(f"Cannot toggle focussing for {self}, the state must be DIVIDED")


class SingleBlock:

    @dispatch(object)
    def __init__(self, block):
        if block is not None and isinstance(block, SingleBlock):
            self.x_axis = block.x_axis
            self.y_axis = block.y_axis
        else:
            raise Exception("Some fields are invalid to initialize a single block")

    @dispatch(int, int)
    def __init__(self, x_axis, y_axis):
        self.x_axis = int(x_axis)
        self.y_axis = int(y_axis)

    def __str__(self) -> str:
        return f"SB ({self.x_axis}, {self.y_axis} -- add: {id(self)})"

    def __eq__(self, o) -> bool:
        if not isinstance(o, SingleBlock):
            return False
        return self.x_axis == o.x_axis and self.y_axis == o.y_axis

    def set_position(self, x_axis, y_axis):
        self.x_axis = x_axis
        self.y_axis = y_axis

    def move_up(self, step=1):
        if isinstance(step, int):
            self.y_axis += step

    def move_down(self, step=1):
        if isinstance(step, int):
            self.y_axis -= step

    def move_left(self, step=1):
        if isinstance(step, int):
            self.x_axis -= step

    def move_right(self, step=1):
        if isinstance(step, int):
            self.x_axis += step

