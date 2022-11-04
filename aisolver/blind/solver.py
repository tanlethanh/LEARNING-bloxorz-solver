from aisolver.blind.frontier import Frontier
from aisolver.blind.state import State


class Solver:

    explored: list[State]

    def __init__(self, frontier: Frontier, initial_state: State) -> None:
        self.frontier = frontier
        self.initial_state = initial_state
        self.frontier.append(initial_state)
        self.explored = []

    # Solve the problem by provided frontier
    # Return all steps from initial state to final state
    def solve(self):
        while not self.frontier.is_empty():
            current_state = self.frontier.pop()
            self.explored.append(current_state)
            if current_state.is_goal():
                return Solver.solution(current_state)
            
            neighbours = current_state.neighbours()

            for next_state in neighbours:
                if self.frontier.contains(next_state) or self.is_explored(next_state):
                    continue
                self.frontier.append(next_state)
        return None

    # This function check whether the state is explored or not.
    # The state must be defined __eq__()
    def is_explored(self, state: State):
        for explored_state in self.explored:
            if state == explored_state:
                return True
        return False

    # Use backtracking to get the solution by goal state
    @staticmethod
    def solution(current_state: State):
        steps = []
        while current_state.parent is not None:
            steps.append(current_state.parent_action)
            current_state = current_state.parent
        steps.reverse()
        return steps

                
                


