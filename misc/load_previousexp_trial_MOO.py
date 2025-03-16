"""
Load Previous Experiment Trials
=============
Load the parameters and metric from the previous experiment trials

"""
import json

def load_previousexp_trial_MOO(json_files, first_objective_name, second_objective_name):
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
        tmd_value_0 = t2['mean']['0']
        sem_value_0 = t2['sem']['0']
        tmd_value_1 = t2['mean']['1']
        sem_value_1 = t2['sem']['1']
        
        # Create the desired dictionary
        result = {first_objective_name: (float(tmd_value_0), float(sem_value_0)), second_objective_name: (float(tmd_value_1), float(sem_value_1))}
        raw_data.append(result)
        parameters.append(param_g)
    
    return parameters, raw_data

####TEST####
# json_files = "C:\\Users\\barkur\\Desktop\\CodeDump\\2024-01-03_08-54-16_BearingOptiupto_43_trial.json"
# first_objective_name = "X-direction"
# second_objective_name = "Y-direction"
# good, dead = load_previousexp_trial_MOO(json_files, first_objective_name, second_objective_name)