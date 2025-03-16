"""
JSON Scatter Plotter
=============
PLots a scatter plot for the data from ".JSON" file belonging
to optimization.
"""

import json
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import scipy.stats as stats
"""
The JSON scatter plotter searches the parameters values for each trial, each arm
and plots them along with the mean. The plot shows the values of each parameters
over the entire trails.
"""

def json_parameter_scatter(file_name, num_trials, arm_number):
    """
    

    Parameters
    ----------
    file_name : TYPE
        DESCRIPTION.
    num_trials : TYPE
        DESCRIPTION.
    arm_number : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    """
    Open the ".json" file and store it in data
    """
    with open(file_name, 'r') as file:
        data = json.load(file)
    """
    Create arrays for parameter names, trails taken amd the total arms used
    """
    x_parameters = [f'x{i}' for i in range(1, 15)]
    trials_taken = [str(i) for i in range(num_trials)]
    total_arms = [arm_number]

    """
    Create a dictionary varible each being an empty list
    """
    variables = {f'x{i}': [] for i in range(1, 15)}
    
    
    """
    Start the loop and append the data to variable
    """
    for para, vari in zip(x_parameters, variables.values()):
        for trial in trials_taken:
            for arm in total_arms:
                name = data['trials'][trial]['generator_run_structs'][0]['generator_run']['arms'][arm]['parameters'][para]
                vari.append(name)

    """
    Create parameter name arrays to insert them a labels during plotting
    """
    param_names = [
        "x_Coordinate",
        "y_Coordinate",
        "Theta_1",
        "Theta_2",
        "Theta_3",
        "Theta_4",
        "Width_1",
        "Width_2",
        "Width_3",
        "Width_4",
        "Height_1",
        "Height_2",
        "Height_3",
        "Height_4"
    ]
    
    """
    Calculate the mean and plot the parameters values over the trails
    """
    for i in range(14):
        var_name = f'x{i + 1}'
        x_values = variables[var_name]

        # Calculate the mean of the current variable
        mean_x = np.mean(x_values)

        # Create a scatter plot
        plt.figure(figsize=(8, 6))
        plt.scatter(range(len(x_values)), x_values, label=f'{var_name} Values', alpha=0.7)
        plt.axhline(y=mean_x, color='red', linestyle='--', label=f'Mean {var_name}:{mean_x:.4f}', linewidth=2)
        plt.xlabel('Iteration')
        plt.ylabel(f'{var_name} Values')
        plt.title(f'Scatter Plot of {param_names[i]} Values with Mean')
        plt.legend()
        plt.savefig(f'optimizationresults_plots/{param_names[i]}_values')
        plt.show()