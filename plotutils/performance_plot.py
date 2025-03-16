"""
Performance Plots
=============
PLots a single plot which shows the variation of the objective (minimization/maximization)
over the range of iterations.
"""

import numpy as np
import matplotlib.pyplot as plt

def plot_acceleration(accel_data, label, frequencies, num_trials):
    """
    

    Parameters
    ----------
    accel_data : TYPE
        DESCRIPTION.
    label : TYPE
        DESCRIPTION.
    frequencies : TYPE
        DESCRIPTION.
    num_trials : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    
    """
    Define a list of line styles, markers, and colors to use
    """
    line_styles = ['-', '--', '-.', ':']
    markers = ['o', 's', 'D', 'v', '^', '>', '<', 'p', '*', 'h']

    """
    Use the default color cycle for distinct colors
    """
    prop_cycle = plt.rcParams['axes.prop_cycle']
    colors = prop_cycle.by_key()['color']
    global accel_max
    accel_max = []

    for row in range(num_trials):
        """
        Extract the acceleration values for the current iteration in the loop
        """
        acceleration = accel_data[row, :]
        accel_max.append(np.max(acceleration))
        
        """
        Choose line style, marker, and color from the predefined lists
        """
        line_style = line_styles[row % len(line_styles)]
        marker = markers[row % len(markers)]
        color = colors[row % len(colors)]
        """
        Darken iteration 1 and the last iteration by reducing alpha (transparency)
        """
        alpha = 1 if row in [0, num_trials - 1] else 0.2
        """
        Plot the acceleration values against the frequencies with the chosen style
        """
        plt.plot(frequencies, acceleration, label=f'Iteration {row+1}', linestyle=line_style, marker=marker, color=color, alpha=alpha)
    
    """
    Set labels, title, legends and grid
    """
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Acceleration')
    plt.title(f'{label} vs. Frequency for Different Iterations')
    plt.legend()
    plt.grid(True)
    plt.show()
    plt.savefig(f'optimizationresults_plots/{label}_vs_frequency_over_iterations')