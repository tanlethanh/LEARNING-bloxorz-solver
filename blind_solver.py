from bloxorz.block import DoubleBlock, DoubleBlockState
from bloxorz.game_board import GameBoard
from bloxorz.tile import BridgeState
from frontier import Frontier
from state import State, Action


class BlindSolver:

    frontier: Frontier

    def __init__(self, frontier, game_board, initial_position, state_brides):
        if not isinstance(frontier, Frontier) or not isinstance(game_board, GameBoard):
            raise Exception("frontier is invalid!")

        initial_block = DoubleBlock(initial_position)
        if state_brides is None:
            list_state_of_bridges = [False] * len(game_board.bridges)
        else:
            list_state_of_bridges = state_brides
        self.initial_state = State(initial_block, list_state_of_bridges)
        self.explored = []
        self.frontier = frontier
        self.game_board = game_board

        self.frontier.append(self.initial_state)

    def solve(self):
        while True:
            # if frontier is empty, we cannot go next. Game over!
            if self.frontier.is_empty():
                print("Cannot solve!")
                return -1

            current_state = self.frontier.remove()
            if not isinstance(current_state, State):
                raise Exception("current state is invalid")

            # add to explored list
            self.explored.append(current_state)

            # we need to update the map
            # because all State use the same map
            self.game_board.update_map(current_state.list_state_all_bridge)
            self.game_board.print_game_board(current_state.block)
            print(self.frontier)

            if self.game_board.is_goal(current_state.block):
                return self.result(current_state)

            # append all valid neighbors of current state to frontier
            neighbors_of_current_state = self.neighbors(current_state)
            for state in neighbors_of_current_state:
                if not self.is_explored(state) and not self.is_in_frontier(state):
                    self.frontier.append(state)

    def result(self, current_state):
        steps = []
        while current_state.parent_state is not None:
            steps.append(current_state.parent_action.name)
            current_state = current_state.parent_state

        steps.reverse()
        return steps

    def neighbors(self, current_state):
        neighbors = []
        for action in Action:
            next_state = self.new_state_after_take_action(current_state, action)
            if next_state is not None:
                neighbors.append(next_state)
        return neighbors

    def is_explored(self, state):
        for explored_state in self.explored:
            if state == explored_state:
                return True
        return False

    def is_in_frontier(self, state):
        return self.frontier.contains(state)

    def new_state_after_take_action(self, current_state, action):
        if current_state.block.state != DoubleBlockState.DIVIDED and action == Action.TOGGLE_FOCUSSING:
            return None

        next_state = State(
            block=DoubleBlock(current_state.block),
            list_state_all_bridge=current_state.list_state_all_bridge,
            parent_state=current_state,
            parent_action=action
        )

        is_valid_move = next_state.move(self.game_board, action=action)
        if is_valid_move:
            return next_state
        return None

