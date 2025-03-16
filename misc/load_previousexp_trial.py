"""
Load Previous Experiment Trials
=============
Load the parameters and metric from the previous experiment trials

"""
import json

def load_previousexp_trial(json_files, objective_name):
    """
    

    Parameters
    ----------
    json_files : str - path to the previous experiment json file.
    objective_name : Objective name of the experiment

    Returns
    -------
    parameters : list of parameters.
    raw_data : list of metrics.

    """

    with open(json_files, 'r') as json_file:
        data = json.load(json_file)
    
    trial_data = data['experiment']['data_by_trial']
    num_of_trials = len(trial_data)
    
    trial_list = []
    for i in range(num_of_trials):
        trial_list.append(str(i))
    
    parameters = []
    raw_data = []
    
    for trialnum in trial_list:
        param_g = data['experiment']['trials'][trialnum]['generator_run']['arms'][0]['parameters']
        t = data['experiment']['data_by_trial'][trialnum]['value'][0][1]['df']['value']#['metric_name']["0"]
        t2 = json.loads(t)
        tmd_value = t2['mean']['0']
        sem_value = t2['sem']['0']
        
        # Create the desired dictionary
        result = {objective_name: (float(tmd_value), float(sem_value))}
        raw_data.append(result)
        parameters.append(param_g)
    
    return parameters, raw_data
