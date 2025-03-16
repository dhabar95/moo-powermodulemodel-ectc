"""
Model Performance Plot
=============
Plots the performance of the model over iterations

"""
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np



def model_performance(mean_values_json, trial_index, pdf_performance_data_file, first_objective_name, second_objective_name = None, third_objective_name = None, multiobjective = False):
    """
    
    
    Parameters
    ----------
    values : TYPE
        DESCRIPTION.
    save_location : TYPE
        DESCRIPTION.
    
    Returns
    -------
    TYPE
        DESCRIPTION.
    
    """
    
    mean_values_list = mean_values_json.tolist()

    
    if multiobjective == True:
    
        value_objective_1 = [row[0] for row in mean_values_list]
        value_objective_2 = [row[1] for row in mean_values_list]

    
        
        
        if third_objective_name is not None:
            
            value_objective_3 = [row[2] for row in mean_values_list]
    
        
        for i in range(len(mean_values_list[0])):
            if i == 0:
                objective_name = first_objective_name
                save_location = pdf_performance_data_file.replace(".pdf", f"_{objective_name}_normal.pdf")
                values = value_objective_1
                
           
            if i == 1:
                objective_name = second_objective_name
                save_location = pdf_performance_data_file.replace(".pdf", f"_{objective_name}_normal.pdf")
                values = value_objective_2
                
            
            if i == 2:
                objective_name = third_objective_name
                save_location = pdf_performance_data_file.replace(".pdf", f"_{objective_name}_normal.pdf")
                values = value_objective_3
                
        
    
            x_values = list(range(1, len(values) + 1))
            """
            Initialize a list for the monotonic curve.
            """
            monotonic_curve = [values[0]]
            """
            Iterate through the values to create the monotonic curve.
            """
            for value in values[1:]:
                """
                Check if the current value is less than or equal to the previous one.
                """
                if value <= monotonic_curve[-1]:
                    monotonic_curve.append(value)
                else:
                    monotonic_curve.append(monotonic_curve[-1])
        
            """
            x-, y- axis range.
            """
        
            min_value_y = min(monotonic_curve)
            max_value_y = max(monotonic_curve)
        
            percentage_increase_y = 0.15  # 15% increase
            new_min_y = min_value_y - (percentage_increase_y * min_value_y)
            new_max_y = max_value_y + (percentage_increase_y * max_value_y)
        
            y_axis_range = [new_min_y, new_max_y]
        
        
            max_value_x = max(x_values)
        
            percentage_increase_x = 0.15  # 15% increase
            new_max_x = max_value_x + (percentage_increase_x * max_value_x)
        
            x_axis_range = [0, new_max_x]
            
            # Create a single plot with both curves
            plt.figure(figsize=(6, 4))  # Optional: Set the figure size
    
            # Plot the first curve
            plt.plot(x_values, monotonic_curve, label=" With monotonic constraints", color='blue')

    
            # Plot the second curve on top of the first one
            plt.plot(x_values, values, label='Without monotonic constraints', color='red')

            # Customize the plot
            plt.title('Optimization Trace', fontname='Times New Roman', fontsize=16)
            plt.xlabel('Trials', fontname='Times New Roman', fontsize=14)
            plt.ylabel(objective_name,fontname='Times New Roman', fontsize=14)
            plt.legend(prop={'family': 'Times New Roman', 'size': 12})
            
            # Set the font for x and y axis tick labels
            plt.xticks(fontname='Times New Roman', fontsize=12)
            plt.yticks(fontname='Times New Roman', fontsize=12)
    
            # Show the plot
            plt.grid(False)
            plt.savefig(save_location)
            plt.close()
            
    
    else:
        objective_name = first_objective_name
        save_location = pdf_performance_data_file.replace(".pdf", f"upto_{trial_index}_trial_{first_objective_name}_normal.pdf")
        values = [item for sublist in mean_values_list for item in sublist]
    
        x_values = list(range(1, len(values) + 1))
        """
        Initialize a list for the monotonic curve.
        """
        monotonic_curve = [values[0]]
        """
        Iterate through the values to create the monotonic curve.
        """
        for value in values[1:]:
            """
            Check if the current value is less than or equal to the previous one.
            """
            if value <= monotonic_curve[-1]:
                monotonic_curve.append(value)
            else:
                monotonic_curve.append(monotonic_curve[-1])
    
        """
        x-, y- axis range.
        """
    
        min_value_y = min(monotonic_curve)
        max_value_y = max(monotonic_curve)
    
        percentage_increase_y = 0.15  # 15% increase
        new_min_y = min_value_y - (percentage_increase_y * min_value_y)
        new_max_y = max_value_y + (percentage_increase_y * max_value_y)
    
        y_axis_range = [new_min_y, new_max_y]
    
    
        max_value_x = max(x_values)
    
        percentage_increase_x = 0.15  # 15% increase
        new_max_x = max_value_x + (percentage_increase_x * max_value_x)
    
        x_axis_range = [0, new_max_x]
        
        # Create a single plot with both curves
        plt.figure(figsize=(6, 4))  # Optional: Set the figure size

        # Plot the first curve
        plt.plot(x_values, monotonic_curve, label=" With monotonic constraints", color='blue')

        # Plot the second curve on top of the first one
        plt.plot(x_values, values, label='Without monotonic constraints', color='red')

        # Customize the plot
        plt.title('Optimization Trace', fontname='Times New Roman', fontsize=16)
        plt.xlabel('Trials', fontname='Times New Roman', fontsize=14)
        plt.ylabel(objective_name,fontname='Times New Roman', fontsize=14)
        plt.legend(prop={'family': 'Times New Roman', 'size': 12})
        
        # Set the font for x and y axis tick labels
        plt.xticks(fontname='Times New Roman', fontsize=12)
        plt.yticks(fontname='Times New Roman', fontsize=12)

        # Show the plot
        plt.grid(False)
        plt.savefig(save_location)
        plt.close()





























































