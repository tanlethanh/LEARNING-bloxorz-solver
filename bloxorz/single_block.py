from multipledispatch import dispatch


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

