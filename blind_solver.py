from bloxorz.block import DoubleBlock, DoubleBlockState
from bloxorz.game_board import GameBoard
from bloxorz.tile import BridgeState
from frontier import Frontier
from state import State, Action


class BlindSolver:

    def __init__(self, frontier, game_board, initial_position):
        if not isinstance(frontier, Frontier) or not isinstance(game_board, GameBoard):
            raise Exception("frontier is invalid!")

        initial_block = DoubleBlock(initial_position=initial_position)
        list_state_of_bridges = [BridgeState.NOT_ACTIVE] * len(game_board.bridges)
        self.initial_state = State(initial_block, list_state_of_bridges)
        self.explored = []
        self.frontier = frontier
        self.game_board = game_board

    def solve(self):
        while True:
            # if frontier is empty, we cannot go next. Game over!
            if self.frontier.is_empty():
                print("Cannot solve!")
                return -1

            current_state = self.frontier.remove()
            if not isinstance(current_state, State):
                raise Exception("current state is invalid")

            # we need to update the map
            # because all State use the same map
            self.game_board.update_map(current_state.list_state_all_bridge)

            if self.game_board.is_goal(current_state.block):
                return self.result(current_state)

            # append all valid neighbors of current state to frontier
            neighbor_of_current_state = self.neighbors(current_state)
            for state in neighbor_of_current_state:
                if not self.is_explored(state) and not self.is_in_frontier(state):
                    self.frontier.append(state)

    def result(self, current_state):
        pass

    def neighbors(self, current_state):
        neighbors = []
        for action in Action.list():
            next_state = self.new_state_after_take_action(current_state, action)
            if next_state is not None and self.game_board.is_valid_position(next_state.block):
                neighbors.append(next_state)
        return neighbors

    def is_explored(self, state):
        for explored_state in self.explored:
            if state.equals(explored_state):
                return True
        return False

    def is_in_frontier(self, state):
        return self.frontier.contains(state)

    def new_state_after_take_action(self, current_state, action):
        if current_state.block.state != DoubleBlockState.DIVIDED and action == Action.TOGGLE_FOCUSSING:
            return None

        next_state = State(
            block=DoubleBlock(block=current_state),
            list_state_all_bridge=current_state.list_state_all_bridge,
            parent_state=current_state,
            parent_action=action
        )

        match action:
            case Action.TURN_UP:
                next_state.turn_up(self.game_board.map)
            case Action.TURN_DOWN:
                next_state.turn_down(self.game_board.map)
            case Action.TURN_LEFT:
                next_state.turn_left(self.game_board.map)
            case Action.TURN_RIGHT:
                next_state.turn_right(self.game_board.map)
            case Action.TOGGLE_FOCUSSING:
                next_state.toggle_focussing(self.game_board.map)
        return next_state

