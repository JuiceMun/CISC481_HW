import matplotlib.pyplot as plt


class Yard:
    """undirected graph to represent the train yard"""
    def __init__(self):
        self.connectivity = {}

    def add_edge(self, a, b):
        """Adds an undirected connection (two-way) between nodes a and b"""

        if a not in self.connectivity:
            self.connectivity[a] = []
        self.connectivity[a].append(b)

        if b not in self.connectivity:
            self.connectivity[b] = []
        self.connectivity[b].append(a)

    def get_yard(self):
        return self.connectivity


def possible_actions(yard, state):
    return None


def draw_yard_matplotlib(yard, positions):
    """
    AI Generated - positions: dict mapping nodes -> (x, y) coordinates
    """
    for node, neighbors in yard.get_yard().items():
        x, y = positions[node]
        plt.scatter(x, y, c="lightblue", s=500)
        plt.text(x, y, node, ha="center", va="center", weight="bold")

        for neighbor in neighbors:
            nx, ny = positions[neighbor]
            plt.plot([x, nx], [y, ny], "k-")  # draw line

    plt.axis("equal")
    plt.show()
