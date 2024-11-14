import networkx as nx
import numpy as np
import pygad
import argparse
import warnings
import matplotlib.pyplot as plt

import numpy as np

def load_qap_data(file_path):
    """
    Load QAP data from a .dat file.
    
    Parameters:
    file_path (str): Path to the .dat file.
    
    Returns:
    tuple: A tuple containing the distance matrix and flow matrix.
    """
    # Open the file to read the size from the first line
    with open(file_path, "r") as file:
        size = int(file.readline().strip())  # Read and convert the first line to an integer

    # Load the remaining data
    data = np.loadtxt(file_path, skiprows=1)

    # Slice the data into distance and flow matrices
    distance_matrix = data[:size, :size]
    flow_matrix = data[size:, :size]

    return distance_matrix, flow_matrix

def load_qap_solution(file_path):
    try:
        with open(file_path, 'r') as file:
            # Read the first line
            first_line = file.readline().strip()
            
            # Split the line into values
            values = first_line.split()
            
            # Return the second value (index 1)
            return int(values[1])
    except FileNotFoundError:
        print(f"Error: The solution file at '{file_path}' does not exist.")
        return 0
    
def fitness_function(ga_instance, solution, solution_idx):
    # Calculate the total cost of the solution based on the flow and distance matrices
    cost = 0
    for i in range(len(solution)):
        for j in range(len(solution)):
            cost += flow_matrix[i, j] * distance_matrix[solution[i], solution[j]]
    return -cost

warnings.filterwarnings("ignore", category=UserWarning)

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Quadratic Assignemt Problem Solver using Genetic Algorithm.")
parser.add_argument("instance", type=str, help="Instance of quadratic assignment problem")
parser.add_argument("-f", "--plot_fitness", action="store_true", help="Plot the fitness graph")
args = parser.parse_args()

# Load data
distance_matrix, flow_matrix = load_qap_data(f"../../problem-instances/quadratic-assignment/instances/{args.instance}.dat")
known_solution_fitness = load_qap_solution(f"../../problem-instances/quadratic-assignment/solutions/{args.instance}.sln")

# Set up the GA parameters
num_genes = len(distance_matrix)  # Number of facilities or locations

ga_instance = pygad.GA(
    num_generations=1000,
    num_parents_mating=50,
    fitness_func=fitness_function,
    sol_per_pop=100,
    num_genes=num_genes,
    gene_type=int,
    gene_space=list(range(num_genes)),
    mutation_type="swap",
    mutation_percent_genes=20,
    parent_selection_type="rws",
    crossover_type="two_points",
    crossover_probability=0.8,
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
print("Fitness of the best found solution:", -solution_fitness)  # Negative to show the minimized cost
print("Gap to best known solution (in %):", ((-solution_fitness / known_solution_fitness) - 1) * 100)  # Negative to show the minimized cost

