import networkx as nx
import numpy as np
import pygad
import argparse
import warnings
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
import math

def load_vrp_data(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    # Find the <nodes> section
    nodes = []
    for node in root.findall(".//node"):
        node_id = int(node.get("id"))
        cx = float(node.find("cx").text)
        cy = float(node.find("cy").text)
        nodes.append({"id": node_id, "cx": cx, "cy": cy})
    
    return nodes

def calculate_distance_matrix(nodes):
    num_nodes = len(nodes)
    distance_matrix = [[0.0] * num_nodes for _ in range(num_nodes)]
    
    for i in range(num_nodes):
        for j in range(num_nodes):
            if i != j:
                x1, y1 = nodes[i]["cx"], nodes[i]["cy"]
                x2, y2 = nodes[j]["cx"], nodes[j]["cy"]
                distance_matrix[i][j] = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
    return distance_matrix
    
def fitness_function(ga_instance, solution, solution_idx):
    # Calculate the total cost of the solution based on the flow and distance matrices
    cost = 0
    for i in range(len(solution)):
        for j in range(len(solution)):
            cost += flow_matrix[i, j] * distance_matrix[solution[i], solution[j]]
    return -cost

warnings.filterwarnings("ignore", category=UserWarning)

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Vehicle Routing Problem Solver using Genetic Algorithm.")
parser.add_argument("instance", type=str, help="Instance of quadratic assignment problem")
parser.add_argument("-f", "--plot_fitness", action="store_true", help="Plot the fitness graph")
args = parser.parse_args()

# Load data
nodes = load_vrp_data(f"../../problem-instances/vehicle-routing/augerat-1995-set-a/{args.instance}.xml")
distance_matrix = calculate_distance_matrix(nodes)
