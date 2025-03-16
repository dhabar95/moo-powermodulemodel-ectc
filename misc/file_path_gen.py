"""
File Path Generator
=============
Generate all the required paths to store the json and pdf files.
"""
import os

class file_path_gen:
    
    
    
    def __init__(self, time_stamp, main_json, main_pdf, number_of_parameters, fixed_para, objective_name):
        """
        

        Parameters
        ----------
        time_stamp : TYPE
            DESCRIPTION.
        main_json : TYPE
            DESCRIPTION.
        main_pdf : TYPE
            DESCRIPTION.
        number_of_parameters : TYPE
            DESCRIPTION.
        objective_name : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        

        self.time_stamp = time_stamp
        self.main_json = main_json
        self.main_pdf = main_pdf
        self.number_of_parameters = number_of_parameters
        self.objective_name = objective_name
        self.fixed_para = fixed_para
        
    def data_filepath_gen(self):
        """
        

        Returns
        -------
        json_data_path : TYPE
            DESCRIPTION.

        """
        
        json_data_path = os.path.join(self.main_json, f"{self.time_stamp}_{self.objective_name}.json")
        
        return json_data_path
    
    def performance_filepath_gen(self):
        """
        

        Returns
        -------
        json_performance_data_file : TYPE
            DESCRIPTION.
        pdf_performance_data_file : TYPE
            DESCRIPTION.

        """
        
        json_performance_data_file = os.path.join(self.main_json, f"{self.time_stamp}_{self.objective_name}_performance_plots.json")
        pdf_performance_data_file = os.path.join(self.main_pdf, f"{self.time_stamp}_{self.objective_name}_performance_plots.pdf")
        
        return json_performance_data_file, pdf_performance_data_file
    
    def crossvalidation_filepath_gen(self):
        """
        

        Returns
        -------
        json_crossvalidation_data_file : TYPE
            DESCRIPTION.
        pdf_crossvalidation_data_file : TYPE
            DESCRIPTION.

        """
        
        json_crossvalidation_data_file = os.path.join(self.main_json, f"{self.time_stamp}_{self.objective_name}_cross_validation.json")
        pdf_crossvalidation_data_file = os.path.join(self.main_pdf, f"{self.time_stamp}_{self.objective_name}_cross_validation.pdf")
        
        return json_crossvalidation_data_file, pdf_crossvalidation_data_file
    
    
    def modelbelief_filepath_gen(self):
        """
        

        Returns
        -------
        json_crossvalidation_data_file : TYPE
            DESCRIPTION.
        pdf_crossvalidation_data_file : TYPE
            DESCRIPTION.

        """
        
        
        pdf_modelbelief_file = os.path.join(self.main_pdf, f"{self.time_stamp}_{self.objective_name}_model_belief.pdf")
        pdf_modelbelief_zoomed_file = os.path.join(self.main_pdf, f"{self.time_stamp}_{self.objective_name}_model_belief_zoomed.pdf")
        
        return pdf_modelbelief_file, pdf_modelbelief_zoomed_file
    
    def pareto_filepath_gen(self):
        """
        

        Returns
        -------
        json_pareto_file : TYPE
            DESCRIPTION.
        pdf_pareto_file : TYPE
            DESCRIPTION.

        """
        
        
        pdf_pareto_file = os.path.join(self.main_pdf, f"{self.time_stamp}_{self.objective_name}_MOO_pareto.pdf")
        json_pareto_file = os.path.join(self.main_json, f"{self.time_stamp}_{self.objective_name}_MOO_pareto.json")
        
        return pdf_pareto_file, json_pareto_file
    
    
    def surfaceresponse_filepath_gen(self):
        """
        

        Returns
        -------
        json_srplot_files : TYPE
            DESCRIPTION.
        pdf_srplot_files : TYPE
            DESCRIPTION.

        """

        json_srplot_files = []
        pdf_srplot_files = []


        for i in range(1, self.number_of_parameters + 1):
            if i not in self.fixed_para:
                for j in range(i + 1, self.number_of_parameters + 1):
                    if j not in self.fixed_para:
                    

                        file_path_srplots = os.path.join(self.main_json, f"{self.time_stamp}_{self.objective_name}_surfaceresponse_x{i}_vs_x{j}_plots.json")
                        pdf_file_name_srplots = os.path.join(self.main_pdf, f"{self.time_stamp}_{self.objective_name}_surfaceresponse_x{i}_vs_x{j}_plots.pdf")
                        
        
                        json_srplot_files.append(file_path_srplots)
                        pdf_srplot_files.append(pdf_file_name_srplots)

        return json_srplot_files, pdf_srplot_files
    
    
    
    def slice_plot_filepath_gen(self):
        """
        Parameters
        ----------
        time_stamp : Pass the time_stamp variable which is defined initially.
        main_json : The main JSON folder where other JSON datas are stored.
        main_pdf : The main PDF folder where other PDF plots datas are stored.
        number_of_parameters : Enter the number of parameters used in the optimization.
    
        Returns
        -------
        json_sliceplot_files : A list of json file paths for each parameter slice plot.
        pdf_sliceplot_files : A list of pdf file paths for each parameter slice plot.
    
        """
        """
        Create an empty list to store all the file paths
        """
        json_sliceplot_files = []
        pdf_sliceplot_files = []
        """
        Create a loop to generate the file path
        """
        for i in range(1, self.number_of_parameters+1):
            
            file_name_sliceplot = f"{self.time_stamp}_{self.objective_name}_slice_x{i}_plots.json"
            pdf_file_name_slicplot = f"{self.time_stamp}_{self.objective_name}_slice_x{i}_plots.pdf"
            
            file_path = os.path.join(self.main_json, file_name_sliceplot)
            pdf_file_path = os.path.join(self.main_pdf, pdf_file_name_slicplot)
            
            json_sliceplot_files.append(file_path)
            pdf_sliceplot_files.append(pdf_file_path)
        """
        Retrun the list of file paths
        """
        return json_sliceplot_files, pdf_sliceplot_files
        
    def generate_all(self):
        """
        

        Returns
        -------
        path_json_data : TYPE
            DESCRIPTION.
        path_json_performance : TYPE
            DESCRIPTION.
        path_pdf_performance : TYPE
            DESCRIPTION.
        path_json_crossvalidation : TYPE
            DESCRIPTION.
        path_pdf_crossvalidation : TYPE
            DESCRIPTION.
        path_json_surfaceresponse : TYPE
            DESCRIPTION.
        path_pdf_surfaceresponse : TYPE
            DESCRIPTION.
        path_json_sliceplot : TYPE
            DESCRIPTION.
        path_pdf_sliceplot : TYPE
            DESCRIPTION.

        """
        
        path_json_data = self.data_filepath_gen()
        path_json_performance, path_pdf_performance = self.performance_filepath_gen()
        path_json_crossvalidation, path_pdf_crossvalidation = self.crossvalidation_filepath_gen()
        path_json_surfaceresponse, path_pdf_surfaceresponse = self.surfaceresponse_filepath_gen()
        path_json_sliceplot, path_pdf_sliceplot = self.slice_plot_filepath_gen()
        path_pdf_modelbelief, path_pdf_modelbelief_zoomed = self.modelbelief_filepath_gen()
        path_pdf_pareto, path_json_pareto = self.pareto_filepath_gen()
        
        return path_json_data, path_json_performance, path_pdf_performance, path_json_crossvalidation, path_pdf_crossvalidation, path_json_surfaceresponse, path_pdf_surfaceresponse, path_json_sliceplot, path_pdf_sliceplot, path_pdf_modelbelief, path_pdf_modelbelief_zoomed, path_pdf_pareto, path_json_pareto
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        