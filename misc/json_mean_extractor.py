"""
JSON-mean extractor
=============
The foloowing function extracts the mean per trial per arm and stores it in an array where rows
represents the trials and column(s) represent the mean value for the specific arm.
"""
import json
import numpy as np
"""
Below is an example on how you can look for the file path and pass it as 
an argument to the funtion
----
parent_dir = os.path.dirname(os.getcwd())
exampledata_filepath = os.path.join(parent_dir, "examples", "exampledata", "TMD_26trials.json")
----
"""
def json_mean_extractor(exampledata_filepath):
    """
    

    Parameters
    ----------
    exampledata_filepath : TYPE
        DESCRIPTION.

    Returns
    -------
    mean_per_trial_array : TYPE
        DESCRIPTION.

    """


    with open(exampledata_filepath, 'r') as file:
        data = json.load(file)
        """
        Distinguising between the JSON file when stored using "save_experiment()"
        and  "ax_client.save_to_json_file()"
        """
    
        if "experiment" in data:
            
            total_trials = len(data['experiment']['trials'])
            number_list = [str(num) for num in range(total_trials)]
            
            mean_per_trial = []
            
            for trial in number_list:
                json_string = data['experiment']['data_by_trial'][trial]['value'][0][1]['df']['value']
                data_string = json.loads(json_string)
                arms_number = len(data_string['mean'])
                """
                Extract the mean values
                """
                mean_values = [float(data_string['mean'][str(i)]) for i in range(arms_number)]
                """
                Append mean values to mean_per_trial as a list
                """
                mean_per_trial.append(mean_values)
            
            """
            Convert the list to a np array
            """
            mean_per_trial_array = np.array(mean_per_trial)

            
        else:
            total_trials = len(data['trials'])
            number_list = [str(num) for num in range(total_trials)]
            
            mean_per_trial = []
            
            for trial in number_list:
                json_string = data['data_by_trial'][trial]['value'][0][1]['df']['value']
                data_string = json.loads(json_string)
                arms_number = len(data_string['mean'])

                mean_values = [float(data_string['mean'][str(i)]) for i in range(arms_number)]
                
                mean_per_trial.append(mean_values)

            mean_per_trial_array = np.array(mean_per_trial)
            
        
        return mean_per_trial_array
