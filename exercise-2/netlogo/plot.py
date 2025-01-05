import argparse
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def plot_graphs(variable_name): 
    # Load the CSV file
    file_path = f'spreadsheets/NetLogo_PSO_Playground {variable_name}-table.csv'
    file_path_nc = f'spreadsheets/NetLogo_PSO_Playground {variable_name}-nc-table.csv'

    data = pd.read_csv(file_path, skiprows=6)
    data_nc = pd.read_csv(file_path_nc, skiprows=6)

    # Clean and process the data
    data[variable_name] = data[variable_name].astype(float)
    data_nc[variable_name] = data_nc[variable_name].astype(float)

    # Unique fitness functions and constraints
    fitness_functions = data['fitness_function'].unique() 
    constraints = data['Constraint'].unique() 

    # Define the limits for the x-axis (iterations)
    x_min = 0  # Set your minimum value for x-axis
    x_max = 35  # Set your maximum value for x-axis

    unique_variable_sizes = sorted(data[variable_name].unique())
    markers = ["o", "s", "8"]
    marker_dict = dict(zip(unique_variable_sizes, markers))

    colors = ["tab:orange", "tab:blue", "tab:green"]
    colors_dict = dict(zip(unique_variable_sizes, colors))

    # Create the figure and the grid of subplots
    fig, axs = plt.subplots(len(fitness_functions), len(constraints) + 1, figsize=(15, 12))

    for i, fitness_function in enumerate(fitness_functions):
        subset = data_nc[(data_nc['fitness_function'] == fitness_function)]

        # Sort variable sizes for a sorted legend
        sorted_variable_sizes = sorted(subset[variable_name].unique())
        
        # Plot each population size
        for variable_size in sorted_variable_sizes:
            pop_subset = subset[subset[variable_name] == variable_size]
            axs[i, 0].plot(
                pop_subset['iterations'], 
                pop_subset['global-best-val'], 
                label=f'{variable_name}: {variable_size}', 
                marker=marker_dict[variable_size],
                color=colors_dict[variable_size], 
                linestyle='-',
                alpha=0.6, 
                markersize=6)
            
            # Get the last iteration and value for the vertical line
            last_iteration = pop_subset['iterations'].iloc[-1]

            if last_iteration < x_max: 
                axs[i, 0].axvline(x=last_iteration, color=colors_dict[variable_size], linestyle='--')

        axs[i, 0].set_title(f'{fitness_function} No Constraint Experiment')
        axs[i, 0].set_xlabel('Iterations')
        axs[i, 0].set_ylabel('Best Value')
        axs[i, 0].grid(True)
        axs[i, 0].legend()

        # Conditional x-axis limiting based on x_max
        current_x_max = min(x_max, subset['iterations'].max())
        axs[i, 0].set_xlim(x_min, current_x_max)

    # Plot each fitness function with constraints
    for j, constraint in enumerate(constraints):
        for i, fitness_function in enumerate(fitness_functions):
            subset = data[(data['fitness_function'] == fitness_function) & (data['Constraint'] == constraint)]

            # Sort variable sizes for a sorted legend
            sorted_variable_sizes = sorted(subset[variable_name].unique())

            # Plot each population size
            for variable_size in sorted_variable_sizes:
                pop_subset = subset[subset[variable_name] == variable_size]
                axs[i, j+1].plot(
                    pop_subset['iterations'], 
                    pop_subset['global-best-val'], 
                    label=f'{variable_name}: {variable_size}', 
                    marker=marker_dict[variable_size],
                    color=colors_dict[variable_size], 
                    linestyle='-',
                    alpha=0.6,
                    markersize=6)
                
                # Get the last iteration and value for the vertical line
                last_iteration = pop_subset['iterations'].iloc[-1]

                if last_iteration < x_max: 
                    axs[i, j+1].axvline(x=last_iteration, color=colors_dict[variable_size], linestyle='--')

            axs[i, j+1].set_title(f'{fitness_function} {constraint} Experiment')
            axs[i, j+1].set_xlabel('Iterations')
            axs[i, j+1].set_ylabel('Best Value')
            axs[i, j+1].grid(True)
            axs[i, j+1].legend()

             # Conditional x-axis limiting based on x_max
            current_x_max = min(x_max, subset['iterations'].max())
            axs[i, j+1].set_xlim(x_min, current_x_max)

    plt.tight_layout()
    plt.savefig(f'plots/experiment-{variable_name}.png')

if __name__ == "__main__":
    # Set up argparse to handle command-line arguments
    parser = argparse.ArgumentParser(description="Process CSV file and plot fitness function data.")
    parser.add_argument('variable_name', type=str, help='The variable name of the experiment or all for all figures')

    # Parse the arguments
    args = parser.parse_args()
    input_variable = args.variable_name

    variables = ["particle-inertia", "particle-speed-limit", "personal-confidence", "swarm-confidence", "population-size"]

    if input_variable == "all":
        for variable in variables:
            plot_graphs(variable)
    else:
        plot_graphs(input_variable)