"""
Time and Date Stamp File Name
=============

This script contains a small function, which returns the date and time
which can be used to save the necessary files and not overlap with the previous
results.
"""
import datetime

def time_for_filename():
    """
    

    Returns
    -------
    formatted_time_for_filename : TYPE
        DESCRIPTION.

    """
    """
    Get the current time and date
    """
    current_time = datetime.datetime.now()
    """
    Format it as a string
    """
    formatted_time = current_time.strftime("%Y-%m-%d_%H-%M-%S")
    """
    Replace all the unnecessary formats to underscore ("_").
    """
    formatted_time_for_filename = formatted_time.replace(":", "-").replace(" ", "_")
    """
    Return the formated data and time
    """
    return formatted_time_for_filename