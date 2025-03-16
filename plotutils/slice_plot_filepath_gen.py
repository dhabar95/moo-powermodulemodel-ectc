"""
Slice Plot Path Generator for "n" number of parameters
=============
Generate the required saving file path of slice plots.
"""
import os


def slice_plot_filepath_gen(time_stamp, main_json, main_pdf, number_of_parameters):
    """
    Parameters
    ----------
    time_stamp : Pass the time_stamp variable which is defined initially.
    main_json : The main JSON folder where other JSON datas are stored.
    main_pdf : The main PDF folder where other PDF plots datas are stored.
    number_of_parameters : Enter the number of parameters used in the optimization.

    Returns
    -------
    json_files : A list of json file paths for each parameter slice plot.
    pdf_files : A list of pdf file paths for each parameter slice plot.

    """
    """
    Create an empty list to store all the file paths
    """
    json_files = []
    pdf_files = []
    """
    Create a loop to generate the file path
    """
    for i in range(1, number_of_parameters+1):
        
        file_name = f"{time_stamp}_slice_x{i}_plots.json"
        pdf_file_name = f"{time_stamp}_slice_x{i}_plots.pdf"
        
        file_path = os.path.join(main_json, file_name)
        pdf_file_path = os.path.join(main_pdf, pdf_file_name)
        
        json_files.append(file_path)
        pdf_files.append(pdf_file_path)
    """
    Retrun the list of file paths
    """
    return json_files, pdf_files
