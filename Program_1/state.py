from copy import deepcopy

class State:
    """
    Holds the cars per track (left->right).
    Accepts 'empty' and normalizes it to [].
    """
    def __init__(self, state:str):
        self.state: list = []

        for state in state.split():
            if state == "empty":
                self.state.append([])
            else:
                self.state.append(list(state))

    def __str__(self) -> str:
        return f"state: {self.state}"

    def copy(self):
        """returns a deep copy of the state."""
        copied_state = deepcopy(self.state)
        return copied_state
