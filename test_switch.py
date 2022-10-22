from bloxorz.block import DoubleBlock
from bloxorz.switch import NormalSwitch, SwitchType, SwitchFunction
from bloxorz.tile import Bridge

double_block = DoubleBlock((0, 0))

# test heavy sw
normal_switch = NormalSwitch(1, 1, SwitchType.HEAVY, SwitchFunction.TO_TOGGLE, bridges=[])
bridge_1 = Bridge()
list_state = [False, False, False, False, False, True]
# def test_normal_sw():
