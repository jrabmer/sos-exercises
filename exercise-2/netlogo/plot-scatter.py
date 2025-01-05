import argparse
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def normalizeAndScale(values, scale):
    min_val, max_val = min(values), max(values)
    #return [(x - min_val) / (max_val - min_val) * scale for x in values]
    return [x * scale for x in values]

def plot_graphs(variable_name_1, variable_name_2): 
    # Load the CSV file
    #file_path = f'spreadsheets/NetLogo_PSO_Playground {variable_name_1}-{variable_name_2}-table.csv'
    file_path = "spreadsheets/NetLogo_PSO_Playground personal-confidence-swarm-confidence-table.csv"
    file_path_nc = "spreadsheets/NetLogo_PSO_Playground personal-confidence-swarm-confidence-nc-table.csv"
    data = pd.read_csv(file_path, skiprows=6)
    data_nc = pd.read_csv(file_path_nc, skiprows=6)

    # Clean and process the data
    data[variable_name_1] = data[variable_name_1].astype(float)
    data[variable_name_2] = data[variable_name_2].astype(float)
    data_nc[variable_name_1] = data_nc[variable_name_1].astype(float)
    data_nc[variable_name_2] = data_nc[variable_name_2].astype(float)

    # Unique fitness functions and constraints
    fitness_functions = data['fitness_function'].unique() 
    constraints = data['Constraint'].unique() 

    # Create the figure and the grid of subplots
    fig, axs = plt.subplots(len(fitness_functions), len(constraints) + 1, figsize=(15, 12))

    s_min, s_max = 20, 300

    for i, fitness_function in enumerate(fitness_functions):
        subset = data_nc[(data_nc['fitness_function'] == fitness_function)]

        # Sort variable sizes for a sorted legend
        sorted_variable_1_sizes = sorted(subset[variable_name_1].unique())
        sorted_variable_2_sizes = sorted(subset[variable_name_2].unique())
        
        points = []

        # Plot each population size
        for variable_1_size in sorted_variable_1_sizes:
            for variable_2_size in sorted_variable_2_sizes:
                var_subset = subset[(subset[variable_name_1] == variable_1_size) & (subset[variable_name_2] == variable_2_size)]

                last_values_best_value = []
                last_values_iteration = []

                run_numbers = var_subset['[run number]'].unique() 

                for run in run_numbers:
                    run_subset = var_subset[var_subset['[run number]'] == run]
                    last_values_best_value.append(run_subset["global-best-val"].iloc[-1])
                    last_values_iteration.append(run_subset["iterations"].iloc[-1])
                points.append((variable_1_size, variable_2_size, np.mean(last_values_best_value - np.mean(last_values_iteration) + 200)))

        x, y, s = zip(*points)
        axs[i, 0].scatter(x, y, normalizeAndScale(s, 1), alpha=0.5)
        axs[i, 0].set_title(f'{fitness_function} No Constraint Experiment')
        axs[i, 0].set_xlabel('personal-confidence')
        axs[i, 0].set_ylabel('swarm-confidence')
        axs[i, 0].grid(True)

    # Plot each fitness function with constraints
    for j, constraint in enumerate(constraints):
        for i, fitness_function in enumerate(fitness_functions):
            subset = data[(data['fitness_function'] == fitness_function) & (data['Constraint'] == constraint)]

            # Sort variable sizes for a sorted legend
            sorted_variable_1_sizes = sorted(subset[variable_name_1].unique())
            sorted_variable_2_sizes = sorted(subset[variable_name_2].unique())
            
            points = []

            # Plot each population size
            for variable_1_size in sorted_variable_1_sizes:
                for variable_2_size in sorted_variable_2_sizes:
                    var_subset = subset[(subset[variable_name_1] == variable_1_size) & (subset[variable_name_2] == variable_2_size)]

                    last_values_best_value = []
                    last_values_iteration = []

                    run_numbers = var_subset['[run number]'].unique() 

                    for run in run_numbers:
                        run_subset = var_subset[var_subset['[run number]'] == run]
                        last_values_best_value.append(run_subset["global-best-val"].iloc[-1])
                        last_values_iteration.append(run_subset["iterations"].iloc[-1])
                    
                    points.append((variable_1_size, variable_2_size, np.mean(last_values_best_value) - np.mean(last_values_iteration) + 200))

            x, y, s = zip(*points)
            axs[i, j+1].scatter(x, y, normalizeAndScale(s, 1) , alpha=0.5)
            axs[i, j+1].set_title(f'{fitness_function} {constraint} Experiment')
            axs[i, j+1].set_xlabel('personal-confidence')
            axs[i, j+1].set_ylabel('swarm-confidence')
            axs[i, j+1].grid(True)


    plt.tight_layout()
    plt.savefig(f'plots/experiment-personal-confidence-swarm-confidence.png')

if __name__ == "__main__":
    plot_graphs("personal-confidence", "swarm-confidence")