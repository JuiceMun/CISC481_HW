import matplotlib.pyplot as plt
import networkx as nx
from networkx import cartesian_product


class Yard:
    """undirected graph to represent the train yard"""
    def __init__(self, rail_connectivity:list[list[int]],init_state:list[list[str]],goal_state:list[list[str]]):
        self.rail_connectivity = rail_connectivity
        self.car_positions = init_state
        self.goal_state = goal_state

def possible_actions(yard, state):
    return None

def draw_yard(yard:Yard):
    """creates a chart to display the rail yard"""
    graph:nx.Graph = nx.Graph()

    for current_rail in yard.rail_connectivity:
            graph.add_edge(current_rail[0], current_rail[1])

    #car labels were AI generated
    labels = {}
    for rail in graph.nodes():
        cars = []
        idx = rail - 1
        if 0 <= idx < len(yard.car_positions):
            cars = [c for c in yard.car_positions[idx] if c != "empty"]
        labels[rail] = f"{rail}\n{','.join(cars)}" if cars else str(rail)

    nx.draw_networkx(graph, labels=labels)
    #plt.axis("off")
    plt.show()

