from state import State


class Frontier:

    def __init__(self):
        self.frontier = []

    def is_empty(self):
        if len(self.frontier) == 0:
            return True
        return False

    def append(self, state):
        if not isinstance(state, State):
            print(f"Cannot append {State} to frontier")
        else:
            self.frontier.append(state)

    def contains(self, item):
        for index, state in self.frontier:
            if state.equals(item):
                return True
        return False

    def remove(self):
        pass


class StackFrontier(Frontier):

    def remove(self):
        return self.frontier.pop()


class QueueFrontier(Frontier):

    def remove(self):
        return self.frontier.pop(0)
