import networkx as nx
import numpy as np
import pygad
import argparse
import warnings
import matplotlib.pyplot as plt


warnings.filterwarnings("ignore", category=UserWarning)

# Step 1: Set up command-line arguments
parser = argparse.ArgumentParser(description="3-Colorability Problem Solver using Genetic Algorithm.")
parser.add_argument("node_count", type=int, help="Number of nodes in the instance")
parser.add_argument("-n", "--negative_instance", action="store_true", help="The graph is negative instance (True/False).")
parser.add_argument("-f", "--plot_fitness", action="store_true", help="Plot the fitness graph")
parser.add_argument("-c", "--plot_coloring", action="store_true", help="Plot the coloring graph")

args = parser.parse_args()

# Step 1: Load the graph
G = nx.read_graphml(f"../../problem-instances/3-colorability/graph_{args.node_count}_nodes_{'negative' if args.negative_instance else 'positive'}.graphml")

# Ensure that all nodes are integers
# Create a new dictionary to map existing node IDs to integers
node_mapping = {node: int(node) for node in G.nodes()}

# Now relabel the graph using the mapping
G = nx.relabel_nodes(G, node_mapping)

num_vertices = G.number_of_nodes()
num_edges = G.number_of_edges()

# Step 2: Parameters for the genetic algorithm
num_colors = 3  # For 3-coloring problem

# Step 3: Define the fitness function
def fitness_function(ga_instance, solution, solution_idx):
    """
    Fitness function to count the number of edges with different-colored vertices.
    Higher score indicates fewer conflicts.
    """
    fitness = 0
    for u, v in G.edges():
        # Increase fitness if adjacent nodes have different colors
        if solution[u] != solution[v]:
            fitness += 1
    return fitness / num_edges

# Step 4: Define the genetic algorithm parameters
ga_instance = pygad.GA(
    num_generations=1000,  # Number of generations
    num_parents_mating=10,  # Number of parents to mate
    fitness_func=fitness_function,
    sol_per_pop=10,  # Population size
    num_genes=num_vertices,  # Each gene represents a vertex color

    # Step 5: Define the gene space (colors 0, 1, or 2)
    gene_space=list(range(num_colors)),  # Restrict genes to 0, 1, or 2

    # Step 6: Crossover and mutation methods
    crossover_type="uniform",  # Uniform crossover
    mutation_type="random",  # Random mutation
    gene_type=int
)

# Step 7: Run the genetic algorithm
ga_instance.run()

if args.plot_fitness:
    # After the generations complete, some plots are showed that summarize the how the outputs/fitenss values evolve over generations.
    ga_instance.plot_fitness()

# Step 8: Retrieve and interpret the best solution
solution, solution_fitness, solution_idx = ga_instance.best_solution()

print("Best solution (coloring):", solution)
print("Fitness of the best solution:", solution_fitness)
print("Number of conflicts (edges with same color vertices):", len(G.edges()) - solution_fitness*num_edges)

if args.plot_coloring:
    color_map = ["red", "green", "blue"]
    node_colors = [color_map[solution[node]] for node in G.nodes()]
    nx.draw(G, node_color=node_colors, with_labels=True, node_size=500, font_color="white")
    plt.show()
