import matplotlib.pyplot as plt
import networkx as nx
from state import State
from action import Action
from collections import deque, defaultdict
import heapq


class Yard:
    """Undirected graph representing a train yard with cars and engine states."""

    def __init__(self, rail_connectivity: list, init_state: State, goal_state: State):
        """Initialize yard with connectivity, initial state, and goal state."""
        self.rail_connectivity = [list(edge) for edge in rail_connectivity]
        self.initial_state = init_state
        self.goal_state = goal_state
        self.current_state = State("")
        self.current_state.state = init_state.copy()

    # ---------------- helpers ----------------
    def _connected(self, x: int, y: int) -> bool:
        """Return True if tracks x and y are connected."""
        return [x, y] in self.rail_connectivity or [y, x] in self.rail_connectivity

    def _valid_tracks(self, x: int, y: int) -> bool:
        """Check if x and y are valid track indices (within range and distinct)."""
        n = len(self.current_state.state)
        return 1 <= x <= n and 1 <= y <= n and x != y

    def _engine_on(self, t: int) -> bool:
        """Return True if the engine is currently on track t."""
        return "*" in self.current_state.state[t - 1]

    # ---------------- moves ----------------
    def left(self, y: int, x: int) -> bool:
        """
        Move LEFTMOST car from track y to RIGHT end of track x.
        Returns True if legal move, False otherwise.
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
        if not self.current_state.state[y - 1]:
            print(f"Illegal move - track {y} is empty")
            return False
        car = self.current_state.state[y - 1].pop(0)
        self.current_state.state[x - 1].append(car)
        return True

    def right(self, x: int, y: int) -> bool:
        """
        Move RIGHTMOST car from track x to LEFT/front of track y.
        Returns True if legal move, False otherwise.
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


def possible_actions(yard: Yard, state: State) -> list:
    """Generate all possible actions from a given state under the yard layout."""
    actions = []

    def engine_on(t: int) -> bool:
        return "*" in state.state[t - 1]

    for a, b in yard.rail_connectivity:
        if not (engine_on(a) or engine_on(b)):
            continue
        if state.state[b - 1]:
            actions.append(Action("LEFT", b, a))
        if state.state[a - 1]:
            actions.append(Action("RIGHT", a, b))
    return actions


def result(action: Action, state: State) -> State:
    """Return the new state resulting from applying an action to a state."""
    a, b = action.a - 1, action.b - 1
    tracks = list(state.state)
    ta, tb = list(tracks[a]), list(tracks[b])

    if action.direction == "LEFT":
        car = ta.pop(0)
        tb.append(car)
    elif action.direction == "RIGHT":
        car = ta.pop(-1)
        tb.insert(0, car)
    else:
        raise ValueError("Invalid direction")

    tracks[a], tracks[b] = ta, tb
    s2 = State("")
    s2.state = tracks
    return s2


def expected_states(state: State, yard: Yard) -> list:
    """Return all successor states from a given state in the yard."""
    return [result(action, state) for action in possible_actions(yard, state)]


def _state_key(s: State):
    """Return a hashable key representation of a state (tuple of tuples)."""
    return tuple(tuple(track) for track in s.state)


def dls(yard, current, goal, depth, path, last=None, visited=None, stats=None):
    """Depth-limited search helper for IDDFS."""
    if stats is not None:
        stats["expanded"] += 1
    if visited is None:
        visited = set()
    if current.state == goal.state:
        return True, path
    if depth == 0:
        return False, []

    key = _state_key(current)
    if key in visited:
        return False, []
    visited.add(key)

    for act in possible_actions(yard, current):
        ns = result(act, current)
        found, fpath = dls(yard, ns, goal, depth - 1, path + [act], act, visited, stats)
        if found:
            return True, fpath

    visited.remove(key)
    return False, []


def iterative_deepening_dfs(yard, start_state, goal_state, max_depth, stats=None):
    """Run iterative deepening DFS until depth limit is reached or goal found."""
    if stats is None:
        stats = {"expanded": 0}
    for limit in range(max_depth + 1):
        found, path = dls(yard, start_state, goal_state, limit, [], None, None, stats)
        if found:
            return path, stats
    return [], stats


# ----- Helpers for the heuristic -----
def _adj(rail_connectivity, n):
    """Return adjacency list from rail connectivity list."""
    g = defaultdict(list)
    for x, y in rail_connectivity:
        g[x].append(y)
        g[y].append(x)
    return g


def _bfs_dists(adj, start, n):
    """Compute BFS distances from start to all nodes in adjacency graph."""
    dist = {i: 10**9 for i in range(1, n + 1)}
    dist[start] = 0
    q = deque([start])
    while q:
        u = q.popleft()
        for v in adj[u]:
            if dist[v] == 10**9:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist


def _all_pairs_dists(rail_connectivity, n):
    """Compute all-pairs shortest path distances between tracks."""
    adj = _adj(rail_connectivity, n)
    return {s: _bfs_dists(adj, s, n) for s in range(1, n + 1)}


def _goal_track_map(goal_state: State):
    """Map each car to its goal track index from goal state."""
    mp = {}
    for t_idx, cars in enumerate(goal_state.state, start=1):
        for c in cars:
            if c != "*":
                mp[c] = t_idx
    return mp


def heuristic(state: State, goal_map: dict, dists: dict) -> int:
    """Admissible heuristic: sum of shortest track distances for misplaced cars."""
    h = 0
    for t_idx, cars in enumerate(state.state, start=1):
        for c in cars:
            if c == "*":
                continue
            gtrack = goal_map.get(c)
            if gtrack is not None:
                h += dists[t_idx][gtrack]
    return h


def astar(yard, start=None, goal=None, stats=None):
    """A* search using admissible heuristic; returns plan and stats."""
    if stats is None:
        stats = {"expanded": 0}
    if start is None:
        start = yard.initial_state
    if goal is None:
        goal = yard.goal_state

    def key(s): return tuple(tuple(t) for t in s.state)

    n_tracks = len(start.state)
    dists = _all_pairs_dists(yard.rail_connectivity, n_tracks)
    goal_map = _goal_track_map(goal)

    start_k, goal_k = key(start), key(goal)
    pq, g_cost = [], {start_k: 0}
    heapq.heappush(pq, (heuristic(start, goal_map, dists), 0, 0, start, None, None))
    seen, tie, parent = set(), 1, {}

    while pq:
        f, g, _, s, act, par = heapq.heappop(pq)
        k = key(s)
        if k in seen:
            continue
        seen.add(k)
        stats["expanded"] += 1
        if par is not None:
            parent[k] = (par, act)
        if k == goal_k:
            plan, cur = [], k
            while cur in parent:
                par_k, a = parent[cur]
                plan.append(a); cur = par_k
            plan.reverse()
            return plan, stats

        for a in possible_actions(yard, s):
            s2, k2, g2 = result(a, s), key(result(a, s)), g + 1
            if k2 in g_cost and g2 >= g_cost[k2]:
                continue
            g_cost[k2] = g2
            h2 = heuristic(s2, goal_map, dists)
            heapq.heappush(pq, (g2 + h2, g2, tie, s2, a, k))
            tie += 1

    return [], stats


def draw_yard(yard: Yard):
    """Draw a visual representation of the yard with cars on tracks."""
    graph = nx.Graph()
    for a, b in yard.rail_connectivity:
        graph.add_edge(a, b)

    pos = {}
    for rail in sorted(graph.nodes()):
        x, y = rail - 1, 0
        if any(abs(rail - n) > 1 for n in graph.neighbors(rail)):
            y = 1 if (rail % 2) else -1
        pos[rail] = (x, y)

    labels = {}
    for rail in graph.nodes():
        idx, cars = rail - 1, []
        if 0 <= idx < len(yard.current_state.state):
            cars = yard.current_state.state[idx]
        labels[rail] = f"{rail}\n{','.join(cars)}" if cars else str(rail)

    nx.draw_networkx(graph, pos=pos, labels=labels, node_size=650, node_color="#cfe8ff")
    xs, ys = [p[0] for p in pos.values()], [p[1] for p in pos.values()]
    plt.xlim(min(xs) - 0.5, max(xs) + 0.5)
    plt.ylim(min(ys) - 1.5, max(ys) + 1.5)
    plt.grid(True, which="both", linestyle="--", alpha=0.3)
    plt.title("Debugging chart")
    plt.show()
