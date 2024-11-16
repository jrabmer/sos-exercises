import networkx as nx
import numpy as np
import pygad
import argparse
import warnings
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
import math
import random

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
    total_distance = 0
    # Iterate through the solution to calculate the total distance
    for i in range(len(solution) - 1):
        from_node = solution[i] - 1  # Convert 1-based to 0-based index
        to_node = solution[i + 1] - 1
        total_distance += distance_matrix[from_node][to_node]
    
    # Handle zero distance case to avoid division by zero
    if total_distance == 0:
        return 1e6  # Return a very high fitness value (unlikely case)

    # Return fitness (inverse of total distance, since PyGAD maximizes fitness)
    return 1 / (1 + total_distance)

def order_crossover(parents, offspring_size, ga_instance):
    num_offspring, num_genes = offspring_size
    offspring = np.empty((num_offspring, num_genes), dtype=int)
    
    for i in range(num_offspring):
        # Randomly select two parents
        parent1_idx, parent2_idx = np.random.choice(parents.shape[0], 2, replace=False)
        parent1, parent2 = parents[parent1_idx], parents[parent2_idx]
        
        # Randomly select two crossover points
        start_idx, end_idx = sorted(np.random.choice(num_genes, 2, replace=False))
        
        # Create a copy of parent1 to start with the subsequence
        offspring[i] = -1 * np.ones(num_genes, dtype=int)  # Placeholder for genes

        # Copy the subsequence from parent1 into the offspring
        offspring[i][start_idx:end_idx+1] = parent1[start_idx:end_idx+1]
        
        # Fill the remaining positions in offspring with genes from parent2
        parent2_genes = [gene for gene in parent2 if gene not in offspring[i]]
        
        current_pos = 0
        for j in range(num_genes):
            if offspring[i][j] == -1:  # Empty position
                # Ensure current_pos does not exceed the remaining parent2_genes length
                if current_pos < len(parent2_genes):
                    offspring[i][j] = parent2_genes[current_pos]
                    current_pos += 1
                else:
                    # If current_pos exceeds, break or continue with the next empty position
                    break

    return offspring


def generate_valid_solution(customers, num_vehicles):
    # Randomly shuffle the customer nodes
    random.shuffle(customers)
    
    # Initialize the solution with the depot (1)
    solution = []
    
    # Split customers into vehicles (routes)
    routes = [[] for _ in range(num_vehicles)]
    
    # Distribute customers cyclically across vehicles
    for i, customer in enumerate(customers):
        vehicle_id = i % num_vehicles
        routes[vehicle_id].append(customer)
    
    # Create the solution by adding the depot to each route
    for route in routes:
        # Ensure each route starts and ends with the depot
        route_solution = [1] + route + [1]
        solution.extend(route_solution)
    
    return solution

def draw_solution(start_node, nodes, solution):
    # Create the graph
    G = nx.Graph()

    # Add nodes for nodes
    for node in nodes:
        G.add_node(node['id'], pos=(node['cx'], node['cy']))

    # Parse the solution and create edges
    colors = ['blue', 'green', 'orange']  # Colors for different vehicles
    vehicle_id = 0  # To track which vehicle is being processed
    current_route = []
    for i in range(len(solution) - 1):
        if solution[i] == 1:  # Found a start node (depot), create a new route for the next vehicle
            if current_route:  # Avoid adding empty routes (in case of consecutive start nodes)
                # Add edges for the current route
                for j in range(len(current_route) - 1):
                    G.add_edge(current_route[j], current_route[j + 1], color=colors[vehicle_id])
                vehicle_id += 1  # Move to the next vehicle
            current_route = [solution[i]]  # Start new route
        else:
            current_route.append(solution[i])

    # Add the final route to the graph
    if current_route:
        for j in range(len(current_route) - 1):
            G.add_edge(current_route[j], current_route[j + 1], color=colors[vehicle_id])

    # Get positions of nodes
    pos = nx.get_node_attributes(G, 'pos')

    # Draw the graph
    plt.figure(figsize=(10, 8))

    # Draw nodes (customers) with specific styles
    nx.draw_networkx_nodes(G, pos, node_size=500, node_color='lightblue', alpha=0.8)

    # Draw edges (routes between customers)
    edges = G.edges()
    edge_colors = [G[u][v]['color'] for u, v in edges]  # Color edges based on vehicle
    nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color=edge_colors, width=2, style='solid')

    # Highlight the start point in red (you can repeat this for each vehicle start if needed)
    nx.draw_networkx_nodes(G, pos, nodelist=[1], node_size=700, node_color='red')

    # Draw labels for nodes (customer IDs)
    nx.draw_networkx_labels(G, pos, font_size=10, font_color='black')

    # Title and labels
    plt.title("Vehicle Routing Problem Solution")
    plt.axis('off')

    # Show plot
    plt.show()

warnings.filterwarnings("ignore", category=UserWarning)

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Vehicle Routing Problem Solver using Genetic Algorithm.")
parser.add_argument("instance", type=str, help="Instance of quadratic assignment problem")
parser.add_argument("-f", "--plot_fitness", action="store_true", help="Plot the fitness graph")
parser.add_argument("-s", "--plot_solution", action="store_true", help="Plot the solution graph")
args = parser.parse_args()

# Load data
nodes = load_vrp_data(f"../../problem-instances/vehicle-routing/augerat-1995-set-a/{args.instance}.xml")
distance_matrix = calculate_distance_matrix(nodes)

num_vehicles = 3
customers = []

for node in nodes:
    if node['id'] != 1:
        customers.append(node['id'])

initial_solution = [generate_valid_solution(customers, num_vehicles) for _ in range(100)]

ga_instance = pygad.GA(
    num_generations=100,
    num_parents_mating=50,
    fitness_func=fitness_function,
    gene_type=int,
    initial_population=initial_solution,
    mutation_type="swap",
    parent_selection_type="rws",
    crossover_type="uniform",  # Using custom crossover function
    allow_duplicate_genes=False  # Ensures each facility is assigned uniquely
)

# Run the Genetic Algorithm
ga_instance.run()

if args.plot_fitness:
    # After the generations complete, some plots are showed that summarize the how the outputs/fitenss values evolve over generations.
    ga_instance.plot_fitness()

# Retrieve and print the best solution found
solution, solution_fitness, _ = ga_instance.best_solution()
print("Best solution found:", solution)
print("Fitness of the best found solution:", solution_fitness)  # Negative to show the minimized cost

if args.plot_solution:
    draw_solution(1, nodes, solution)