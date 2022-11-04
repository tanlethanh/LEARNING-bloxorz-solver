from bloxorz.block import SingleBlock


def manhattan_distance(f, s):
    if isinstance(f, SingleBlock) and isinstance(s, SingleBlock):
        return abs(f.x_axis - s.x_axis) + abs(f.y_axis - s.y_axis)
    elif isinstance(f, tuple) and isinstance(s, tuple):
        return abs(f[0] - s[0]) + abs(f[1] - s[1])



