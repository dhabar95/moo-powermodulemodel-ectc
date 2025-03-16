"""
JSON-Data extractor
=============
The following function, extracts the normal JSON data from the stored results.
"""
import json
import sys
sys.path.append('..') 
"""
Below is an example on how you can look for the file path and pass it as 
an argument to the funtion
----
parent_dir = os.path.dirname(os.getcwd())
exampledata_filepath = os.path.join(parent_dir, "examples", "exampledata", "TMD_26trials.json")
----
"""
def json_data_extractor(exampledata_filepath):
    """

    Parameters
    ----------
    exampledata_filepath : TYPE
        DESCRIPTION.

    Returns
    -------
    data : TYPE
        DESCRIPTION.

    """
    """
    Extract and store the data from JSON to variable data.
    """
    with open(exampledata_filepath, 'r') as file:
        data = json.load(file)

    return data
