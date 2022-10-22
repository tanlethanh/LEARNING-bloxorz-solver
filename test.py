import random

from bloxorz.block import SingleBlock, DoubleBlock, DoubleBlockState
from frontier import StackFrontier
from state import Action




frontier = StackFrontier()
frontier.append(1)
frontier.append(3)
frontier.append(4)
frontier.append(9)

print(frontier.frontier)

print(frontier.remove())
print(frontier.remove())