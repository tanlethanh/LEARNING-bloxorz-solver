
class State:

    def __init__(self, parent, parent_action) -> None:
        self.parent = parent
        self.parent_action = parent_action

    def is_goal(self) -> bool:
        pass

    def neighbours(self) -> list:
        pass

    def __eq__(self, o: object) -> bool:
        pass

    def __lt__(self, o: object) -> bool:
        pass

