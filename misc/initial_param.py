"""
Adding Initial Condition as Trial 0
=============
The funcion considers the initial condition as the first trial and continue
generating further the next trials, based on the initial trials.

NOTE: The below code only taken in a "single-set" of parameter as initial parameters
"""
def initial_param(ax_client, param_dict, evaluate):
    """
    

    Parameters
    ----------
    param_dict : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    ax_client.attach_trial(
        parameters=param_dict
    )
    """
    Get the initial parameters and run the trial
    """
    baseline_parameters = ax_client.get_trial_parameters(trial_index=0)
    ax_client.complete_trial(trial_index=0, raw_data=evaluate(baseline_parameters))