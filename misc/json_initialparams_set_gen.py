"""
JSON-initial paramter set generator
=============
The following function, extracts the parameters and their value as a "dict"
format and then returns it. The main use of this is to include already generated 
data-sets as initial sampling.
"""
import json
import sys
import numpy as np
sys.path.append('..') 
"""
Below is an example on how you can look for the file path and pass it as 
an argument to the funtion
----
parent_dir = os.path.dirname(os.getcwd())
exampledata_filepath = os.path.join(parent_dir, "examples", "exampledata", "TMD_26trials.json")
----
"""
def json_initialparams_set_gen(exampledata_filepath):
    """
    

    Parameters
    ----------
    exampledata_filepath : TYPE
        DESCRIPTION.

    Returns
    -------
    values : TYPE
        DESCRIPTION.

    """
    """
    Extract and store the data from JSON to variable data.
    """
    with open(exampledata_filepath, 'r') as file:
        data = json.load(file)
    

    if "experiment" in data:
        """
        From "data" extract the number of trials and arms which is essential in
        accessing the required parameters.
        """
        trials_auto = len(data['experiment']['trials'])
        arms_auto = len(data['experiment']['trials']['0']['generator_run']['arms'])
        """
        Create an array to append all the extracted data belonging to the parameters
        """
        array_of_dicts = []
        """
        Create an index array for the loop
        """
        trial_index = [str(i) for i in range(trials_auto)]
        arm_index = list(range(arms_auto))
        """
        As Ax has two methods of saving JSON , this conditions can be checked
        using the below condition.
        """
        
        for trial in trial_index:
            for arms in arm_index:
                data_dict = data['experiment']['trials'][trial]['generator_run']['arms'][arms]['parameters']
                array_of_dicts.append(data_dict)
    
    else:
        """
        From "data" extract the number of trials and arms which is essential in
        accessing the required parameters.
        """
        trials_auto = len(data['trials'])
        arms_auto = len(data['trials']['0']['generator_run']['arms'])
        """
        Create an array to append all the extracted data belonging to the parameters
        """
        array_of_dicts = []
        """
        Create an index array for the loop
        """
        trial_index = [str(i) for i in range(trials_auto)]
        arm_index = list(range(arms_auto))
        """
        As Ax has two methods of saving JSON , this conditions can be checked
        using the below condition.
        """
        
        for trial in trial_index:
            for arms in arm_index:
                data_dict = data['trials'][trial]['generator_run']['arms'][arms]['parameters']
                array_of_dicts.append(data_dict)
                
    
    """
    Extract all keys with 'x' followed by a number from the first dictionary
    """
    keys = [key for key in array_of_dicts[0] if key.startswith('x')]
    num_columns = len(keys)
    print(f"INFO: {num_columns} parameters are identified")

    """
    Extract values for each key in each iteration and arrange them in a np array
    """
    values = np.array([[d[key] for key in keys] for d in array_of_dicts])
        
    return values