import math
import matplotlib.pyplot as plt
import networkx as nx
from state import State
from action import Action

class Yard:
    """undirected graph to represent the train yard"""
    def __init__(self, rail_connectivity: list, init_state: State, goal_state: State):
        self.rail_connectivity = [list(edge) for edge in rail_connectivity]

        # immutable references for comparison:
        self.initial_state = init_state
        self.goal_state = goal_state

        # mutable working state (copy the list from init_state.copy())
        self.current_state = State("")          # make an empty State
        self.current_state.state = init_state.copy()  # deep-copied list

    # ---------------- helpers ----------------
    def _connected(self, x: int, y: int) -> bool:
        return [x, y] in self.rail_connectivity or [y, x] in self.rail_connectivity

    def _valid_tracks(self, x: int, y: int) -> bool:
        n = len(self.current_state.state)
        return 1 <= x <= n and 1 <= y <= n and x != y

    def _engine_on(self, t: int) -> bool:
        return "*" in self.current_state.state[t - 1]

    # ---------------- moves ----------------
    def left(self, y: int, x: int) -> bool:
        """
        (LEFT y x): Move the LEFTMOST car FROM track y TO the RIGHT end of track x,
        if (x,y) are connected and the engine is on either track.
        """
        # 1 - x and y are in range
        if not self._valid_tracks(x, y):
            print("Illegal move - invalid track(state)")
            return False
        # 2 - x and y are connected
        if not self._connected(x, y):
            print(f"Illegal move - {x},{y} are not connected")
            return False
        # 3 - engine on x or y
        if not (self._engine_on(x) or self._engine_on(y)):
            print(f"Illegal move - engine not on rails {x} or {y}")
            return False
        # 4. source (y) must not be empty
        if not self.current_state.state[y - 1]:
            print(f"Illegal move - track {y} is empty")
            return False
        # 5. take leftmost from y, append to x
        car = self.current_state.state[y - 1].pop(0)
        self.current_state.state[x - 1].append(car)
        return True

    def right(self, x: int, y: int) -> bool:
        """
        RIGHT(x, y): move the LAST car FROM track x TO the LEFT/front of track y,
        if (x,y) connected and engine is on x or y.
        """

        if not self._valid_tracks(x, y):
            print("Illegal move - invalid track(state)")
            return False
        if not self._connected(x, y):
            print(f"Illegal move - {x},{y} are not connected")
            return False
        if not (self._engine_on(x) or self._engine_on(y)):
            print(f"Illegal move - engine not on rails {x} or {y}")
            return False
        if not self.current_state.state[x - 1]:
            print(f"Illegal move - track {x} is empty")
            return False

        car = self.current_state.state[x - 1].pop(-1)
        self.current_state.state[y - 1].insert(0, car)
        return True


def possible_actions(yard: Yard, state: State) -> list[Action]:
    """
    Produce all legal moves (LEFT/RIGHT) from given state `state` under `yard`.
    Returns a list of Action objects.
    """
    actions: list[Action] = []

    def engine_on(t: int) -> bool:
        return "*" in state.state[t - 1]

    for a, b in yard.rail_connectivity:
        # LEFT y x
        if (engine_on(a) or engine_on(b)) and len(state.state[b - 1]) > 0:
            actions.append(Action("LEFT", b, a))

        # RIGHT x y
        if (engine_on(a) or engine_on(b)) and len(state.state[a - 1]) > 0:
            actions.append(Action("RIGHT", a, b))

    return actions

def expected_result(action: Action, state: State) -> State:
    """Returns an expected state based on the input action and state"""

    #1 - deep copy state
    new_state = State("")
    new_state.state = state.state.copy()

    #2 - unpack action
    direction = action.direction
    a = action.a
    b = action.b

    # 3 - do the move by cases
    if direction == "LEFT":
        # see left(y,x)
        car = new_state.state[a - 1].pop(0)
        new_state.state[b - 1].append(car)
    elif direction == "RIGHT":
        # see right(x,y)
        car = new_state.state[a - 1].pop(-1)
        new_state.state[b - 1].insert(0, car)
    else:
        print("Illegal move - invalid direction")
        return State("-1")

    return new_state

def draw_yard(yard: Yard):
    """Visual representation of the yard using CURRENT state."""
    graph = nx.Graph()
    for a, b in yard.rail_connectivity:
        graph.add_edge(a, b)

    # simple generated positions: left->right baseline, branch up/down if needed
    pos = {}
    for rail in sorted(graph.nodes()):
        x = rail - 1
        y = 0
        neighbors = list(graph.neighbors(rail))
        if any(abs(rail - n) > 1 for n in neighbors):
            y = 1 if (rail % 2) else -1
        pos[rail] = (x, y)

    # labels with cars (skip literal "empty" — your State normalized it to [])
    labels = {}
    for rail in graph.nodes():
        idx = rail - 1
        cars = []
        if 0 <= idx < len(yard.current_state.state):
            cars = yard.current_state.state[idx]
        labels[rail] = f"{rail}\n{','.join(cars)}" if cars else str(rail)

    nx.draw_networkx(graph, pos=pos, labels=labels, node_size=650, node_color="#cfe8ff")

    xs = [p[0] for p in pos.values()]
    ys = [p[1] for p in pos.values()]
    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)

    plt.xlim(xmin - 0.5, xmax + 0.5)
    plt.ylim(ymin - 1.5, ymax + 1.5)
    plt.xticks(range(int(xmin), int(xmax) + 1))
    plt.yticks(range(int(ymin) - 1, int(ymax) + 2))
    plt.gca().set_aspect("equal", adjustable="box")
    plt.grid(True, which="both", linestyle="--", alpha=0.3)
    plt.title("Debugging chart")
    plt.show()
