import numpy as np
import matplotlib.pyplot as plt

def json_contour_plot(X1, X2, mean_value):

    
    # Create a grid of X1 and X2 values
    X1, X2 = np.meshgrid(X1, X2)

    
    # Create a contour plot with the original color scheme
    plt.contour(X1, X2, mean_value, levels=20, cmap='jet', linewidths=1.5)
    plt.colorbar()
    
    # Add labels and title
    plt.xlabel('X1')
    plt.ylabel('X2')
    plt.title('2D Contour Plot with Original Mean Value')
    
    # Plot all 50 points of X1 and X2 as black points
    plt.scatter(X1, X2, c='black', s=5, marker='.')
    
    # Create a 1D slice of the plot with X1 on the x-axis
    plt.figure()
    plt.plot(X1[0, :], mean_value[0, :])
    plt.xlabel('X1')
    plt.ylabel('Mean Value')
    plt.title('1D Slice of the Contour Plot (X1 vs. Mean Value)')

    
    plt.show()

    