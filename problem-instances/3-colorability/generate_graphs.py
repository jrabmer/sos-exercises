import networkx as nx
import random
import numpy as np
import matplotlib.pyplot as plt

def save_graph(graph, filename):
    """Save a graph as an edge list in a text file."""
    nx.write_graphml(graph, filename)

def is_3_colorable(graph):
    """Check if a graph is 3-colorable using a backtracking algorithm."""
    colors = {}
    def can_color(node, color):
        for neighbor in graph.neighbors(node):
            if colors.get(neighbor) == color:
                return False
        return True

    def color_graph(node):
        if node == len(graph.nodes):
            return True
        for color in range(3):
            if can_color(node, color):
                colors[node] = color
                if color_graph(node + 1):
                    return True
                del colors[node]
        return False

    return color_graph(0)

def generate_positive_instance(n):
    """Generate a 3-colorable graph."""
    # Use a bipartite graph or a cycle of even length
    if n % 2 == 0:
        return nx.cycle_graph(n)  # Cycles of even length are 3-colorable
    else:
        return nx.bipartite.random_graph(n // 2, n // 2 + 1, 0.3)  # Bipartite graph is always 3-colorable

def generate_negative_instance(n):
    """Generate a non-3-colorable graph."""
    # Generate a dense random graph that is likely non-3-colorable
    while True:
        graph = nx.gnp_random_graph(n, 0.5)
        if not is_3_colorable(graph):  # Keep generating until we find a non-3-colorable instance
            return graph

# Node sizes for which we want to create instances
node_sizes = [5, 10, 25, 50, 100, 200, 500]

for n in node_sizes:
    # Generate a positive (3-colorable) instance
    positive_instance = generate_positive_instance(n)
    positive_filename = f"graph_{n}_nodes_positive.graphml"
    save_graph(positive_instance, positive_filename)
    print(f"Saved positive 3-colorable instance with {n} nodes as {positive_filename}")

    # Generate a negative (non-3-colorable) instance
    negative_instance = generate_negative_instance(n)
    negative_filename = f"graph_{n}_nodes_negative.graphml"
    save_graph(negative_instance, negative_filename)
    print(f"Saved negative non-3-colorable instance with {n} nodes as {negative_filename}")