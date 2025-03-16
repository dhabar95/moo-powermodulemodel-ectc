"""
Adding Initial Condition - Using multiple parameters
=============
The creates an initial sample space for based on a previousl run parameters
"""
def initial_multiparams(ax_client, multiparams_dict, evaluate):
    """
    

    Parameters
    ----------
    param_dict : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    params = multiparams_dict
    params_length = len(params)
    for i in range(params_length):
        ax_client.attach_trial(
            parameters=params[i]
        )
        """
        Get the initial parameters and run the trial
        """
        trial_index = i
        baseline_parameters = ax_client.get_trial_parameters(trial_index)
        ax_client.complete_trial(trial_index, raw_data=evaluate(baseline_parameters))
        print(f"Trial-{trial_index}/{params_length} evaluation completed")