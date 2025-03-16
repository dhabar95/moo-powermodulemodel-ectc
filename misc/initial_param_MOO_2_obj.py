"""
Adding Initial Condition as Trial 0
=============
The funcion considers the initial condition as the first trial and continue
generating further the next trials, based on the initial trials.

NOTE: The below code only taken in a "single-set" of parameter as initial parameters
"""

import numpy as np



class initial_param_MOO_2_obj:
    
    def __init__(self, ax_client, MOO_funtion, param_dict, first_objective_name, second_objective_name):
        
        self.ax_client = ax_client
        self.MOO_funtion = MOO_funtion
        self.first_objective_name = first_objective_name
        self.second_objective_name = second_objective_name
        self.param_dict = param_dict
        

    def evaluation_function(self, parameterization):
        x = np.array([parameterization.get(f"x{i+1}") for i in range(3)])
        multi_obj = self.MOO_funtion(*x)
        # In our case, standard error is 0, since we are computing a synthetic function.
        return {self.first_objective_name: (multi_obj[0], 0.0), self.second_objective_name: (multi_obj[1], 0.0)}

    
    def trial_initiation(self):
        self.ax_client.attach_trial(parameters=self.param_dict)
        baseline_parameters = self.ax_client.get_trial_parameters(trial_index=0)
        self.ax_client.complete_trial(trial_index=0, raw_data=self.evaluation_function(baseline_parameters))
