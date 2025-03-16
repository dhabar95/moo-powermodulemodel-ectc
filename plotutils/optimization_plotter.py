import json
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np
import datetime
from ax.plot.pareto_utils import compute_posterior_pareto_frontier
import matplotlib.colors as mcolors
import matplotlib.font_manager as fm
from matplotlib.colors import Normalize
from matplotlib.cm import viridis


class optimization_plotter:

    def __init__(self, plot_contour, model, plot_slice, parameter_names, 
                 number_of_parameters, first_objective_name, contour_plot_title, 
                 json_srplot_files, pdf_srplot_files, json_sliceplot_files, 
                 pdf_sliceplot_files, pdf_performance_data_file, json_data_path, 
                 contourplot_edit_and_save, sliceplot_edit_and_save, 
                 model_performance, json_mean_extractor, cross_validate, 
                 interact_cross_validation, json_crossvalidation_data_file, 
                 pdf_crossvalidation_data_file, pdf_modelbelief_file, 
                 pdf_modelbelief_zoomed_file, trial_index, fixed_para, 
                 ax_client,
                 pdf_pareto_file, 
                 json_pareto_file,
                 second_objective_name = None, 
                 third_objective_name = None,
                 plot_pareto_frontier = None,
                 multiobjective = False):


        """
        Modules from Ax
        """
        self.plot_contour = plot_contour
        self.model = model
        self.plot_slice = plot_slice
        self.cross_validate = cross_validate
        self.interact_cross_validation = interact_cross_validation
        self.plot_pareto_frontier = plot_pareto_frontier
        self.ax_client = ax_client

        """
        Variables defined
        """
        self.parameter_names = parameter_names
        self.number_of_parameters = number_of_parameters
        self.first_objective_name = first_objective_name
        self.second_objective_name = second_objective_name
        self.third_objective_name = third_objective_name
        self.contour_plot_title = contour_plot_title
        self.trial_index = trial_index
        self.fixed_para = fixed_para
        self.multiobjective = multiobjective

        """
        file paths_initial
        """
        self.json_srplot_files = json_srplot_files
        self.pdf_srplot_files = pdf_srplot_files
        self.json_sliceplot_files = json_sliceplot_files
        self.pdf_sliceplot_files = pdf_sliceplot_files
        self.pdf_performance_data_file = pdf_performance_data_file
        self.json_data_path = json_data_path
        self.json_crossvalidation_data_file = json_crossvalidation_data_file
        self.pdf_crossvalidation_data_file = pdf_crossvalidation_data_file
        self.pdf_modelbelief_file = pdf_modelbelief_file
        self.pdf_modelbelief_file_zoomed = pdf_modelbelief_zoomed_file
        self.pdf_pareto_file = pdf_pareto_file
        self.json_pareto_file = json_pareto_file
        
        """
        file paths_replaced/trial
        """
        
        self.json_srplot_files = [srjsonfilename.replace(".json", f"_upto_{trial_index}_trial.json") for srjsonfilename in self.json_srplot_files]
        self.pdf_srplot_files = [srpdffilename.replace(".pdf", f"_upto_{trial_index}_trial.pdf") for srpdffilename in self.pdf_srplot_files]
        self.json_sliceplot_files = [sljsonfilename.replace(".json", f"_upto_{trial_index}_trial.json") for sljsonfilename in self.json_sliceplot_files]
        self.pdf_sliceplot_files = [slpdffilename.replace(".pdf", f"_upto_{trial_index}_trial.pdf") for slpdffilename in self.pdf_sliceplot_files]
        self.pdf_performance_data_file = self.pdf_performance_data_file.replace(".pdf", f"upto_{self.trial_index}_trial.pdf")
        self.json_data_path = self.json_data_path.replace(".json", f"upto_{self.trial_index}_trial.json")
        self.json_crossvalidation_data_file = self.json_crossvalidation_data_file.replace(".json", f"upto_{self.trial_index}_trial.json")
        self.pdf_crossvalidation_data_file = self.pdf_crossvalidation_data_file.replace(".pdf", f"upto_{self.trial_index}_trial.pdf")
        self.pdf_modelbelief_file = pdf_modelbelief_file.replace(".pdf", f"upto_{self.trial_index}_trial.pdf")
        self.pdf_modelbelief_file_zoomed = pdf_modelbelief_zoomed_file.replace(".pdf", f"upto_{self.trial_index}_trial.pdf")
        
        """
        plotutils
        """
        self.contourplot_edit_and_save = contourplot_edit_and_save
        self.sliceplot_edit_and_save = sliceplot_edit_and_save
        self.model_performance = model_performance
        """
        misc
        """
        self.json_mean_extractor = json_mean_extractor

    def performance_plotter(self):
        print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Generating Performance Plots....")
        mean_values_json = self.json_mean_extractor(self.json_data_path)
        self.model_performance(
            mean_values_json, self.trial_index, self.pdf_performance_data_file, self.first_objective_name, self.second_objective_name, self.third_objective_name, self.multiobjective)

        return print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Performance plots generated and saved succesfully")
   
    def slice_plotter(self):
        print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Generating Slice Plots....")
        if self.second_objective_name is not None and self.third_objective_name is None:
            print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Slice plots generating for 2-Objective Problem")
                        
            for p in range(2):
                if p == 0:
                    self.objective_name = self.first_objective_name
                    print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Slice plots generating for {self.objective_name}")

                if p == 1:
                    self.objective_name = self.second_objective_name
                    print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Slice plots generating for {self.objective_name}")

                    
                for i in range(1, self.number_of_parameters + 1):
                    if i not in self.fixed_para:
                        slice_x = self.plot_slice(self.model, f"x{i}", self.objective_name)
                        slice_x_data = slice_x[0]
                        
                        slice_plot_file_json = self.json_sliceplot_files[i-1].replace(".json", f"{self.objective_name}.json")
                        slice_plot_file_pdf = self.pdf_sliceplot_files[i-1].replace(".pdf", f"{self.objective_name}.pdf")
                        
                        with open(slice_plot_file_json, "w") as json_file_sl1:
                            json.dump(slice_x_data, json_file_sl1)
            
                        self.sliceplot_edit_and_save(slice_plot_file_json, 
                                                      self.parameter_names[f"x{i}"], self.objective_name, slice_plot_file_pdf)
                        print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Slice plots generation complete for {self.objective_name}")
       
       
        if self.third_objective_name is not None and self.second_objective_name is not None:
            print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Slice plots generating for 3-Objective Problem")
            for p in range(3):
                if p == 0:
                    self.objective_name = self.first_objective_name
                    print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Slice plots generating for {self.objective_name}")

                if p == 1:
                    self.objective_name = self.second_objective_name
                    print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Slice plots generating for {self.objective_name}")
                    
                if p == 2:
                    self.objective_name = self.third_objective_name
                    print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Slice plots generating for {self.objective_name}")
                    
                for i in range(1, self.number_of_parameters + 1):
                    if i not in self.fixed_para:
                        slice_x = self.plot_slice(self.model, f"x{i}", self.objective_name)
                        slice_x_data = slice_x[0]
                        
                        slice_plot_file_json = self.json_sliceplot_files[i-1].replace(".json", f"{self.objective_name}.json")
                        slice_plot_file_pdf = self.pdf_sliceplot_files[i-1].replace(".pdf", f"{self.objective_name}.pdf")
                        
                        with open(slice_plot_file_json, "w") as json_file_sl1:
                            json.dump(slice_x_data, json_file_sl1)
            
                        self.sliceplot_edit_and_save(slice_plot_file_json, 
                                                      self.parameter_names[f"x{i}"], self.objective_name, slice_plot_file_pdf)
                        print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Slice plots generation complete for {self.objective_name}")
      
        else:
            print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Slice plots generating for 1-Objective Problem")
            self.objective_name = self.first_objective_name
            print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Slice plots generating for {self.objective_name}")
            for i in range(1, self.number_of_parameters + 1):
                if i not in self.fixed_para:
                    slice_x = self.plot_slice(self.model, f"x{i}", self.objective_name)
                    slice_x_data = slice_x[0]
                    
                    slice_plot_file_json = self.json_sliceplot_files[i-1].replace(".json", f"{self.objective_name}.json")
                    slice_plot_file_pdf = self.pdf_sliceplot_files[i-1].replace(".pdf", f"{self.objective_name}.pdf")
                    
                    with open(slice_plot_file_json, "w") as json_file_sl1:
                        json.dump(slice_x_data, json_file_sl1)
        
                    self.sliceplot_edit_and_save(slice_plot_file_json, 
                                                  self.parameter_names[f"x{i}"], self.objective_name, slice_plot_file_pdf)
                    print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Slice plots generation complete for {self.objective_name}")
 
           

    
        
        return print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Slice plots generated and saved succesfully")


    def cross_validation(self):
        print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Generating Cross-validation Plots....")
        cv_results = self.cross_validate(self.model)
        cv = self.interact_cross_validation(cv_results)
        cv_data = cv[0]
        with open(self.json_crossvalidation_data_file, "w") as json_cv_file:
            json.dump(cv_data, json_cv_file)
             
        if self.second_objective_name is not None and self.third_objective_name is None:
            print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Cross-validation plots generating for 2-Objective Problem")
            for i in [1, 3]:
                
                if i == 1:
                    self.objective_name = self.first_objective_name
                    print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Cross-validation plots generating for {self.objective_name}")

                if i == 3:
                    self.objective_name = self.second_objective_name
                    print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Cross-validation plots generating for {self.objective_name}")

                y_pred = cv_data['data'][i]['y']
                y_actual = cv_data['data'][i]['x']
                min_y = cv_data['data'][0]['x'][0]
                max_y = cv_data['data'][0]['x'][1]
                iterations = np.arange(len(y_actual))  # Assuming iterations are indexed from 0 to n-1
                
                plt.figure(figsize=(6, 4))
                
                # Create a scatter plot with the 'viridis' colormap and colorbar
                norm = Normalize(vmin=0, vmax=len(iterations) - 1)
                scatter = plt.scatter(y_actual, y_pred, c=iterations, cmap=viridis, norm=norm, alpha=0.7, s=80)
                cbar = plt.colorbar(scatter, label='Iterations', orientation='vertical')
                cbar.ax.tick_params(labelsize=12)  # Increase colorbar label font size
                
                # Set the font for the colorbar label to Times New Roman
                font_properties = fm.FontProperties(family='Times New Roman', size=12)
                cbar.set_label('Iterations', fontproperties=font_properties)
                
                plt.plot([min_y, max_y], [min_y, max_y], 'k--', lw=2)
                
                plt.xlabel('Actual Values', fontname='Times New Roman', fontsize=14)
                plt.ylabel('Predicted Values', fontname='Times New Roman', fontsize=14)
                plt.title(f'Cross-validation for {self.objective_name}', fontname='Times New Roman', fontsize=15)
                
                # Set the font for x and y axis labels
                plt.xticks(fontname='Times New Roman', fontsize=12)
                plt.yticks(fontname='Times New Roman', fontsize=12)
                
                # Customize grid and ticks
                plt.grid(True, linestyle='--', alpha=0.5)
                plt.tick_params(axis='both', which='both', bottom=True, top=False, left=True, right=False)
                
                # Add a legend
                plt.legend(['Prediction point', '1:1 Line'], loc='upper left', fontsize=10)
                
                # Set the background color to white
                ax = plt.gca()
                ax.set_facecolor('white')
                
                # Adjust plot layout
                plt.tight_layout()
                
                save_location = self.pdf_crossvalidation_data_file.replace(".pdf", f"{self.objective_name}.pdf")
              
                plt.savefig(save_location, format='pdf', dpi=300, bbox_inches='tight')
                plt.close()
                print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Cross-validation plots generation complete for {self.objective_name}")


        if self.third_objective_name is not None and self.second_objective_name is not None:
            print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Cross-validation plots generating for 2-Objective Problem")

            for i in [1, 3, 5]:
                
                if i == 1:
                    self.objective_name = self.first_objective_name
                    print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Cross-validation plots generating for {self.objective_name}")

                if i == 3:
                    self.objective_name = self.second_objective_name
                    print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Cross-validation plots generating for {self.objective_name}")

                if i == 5:
                    self.objective_name = self.third_objective_name
                    print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Cross-validation plots generating for {self.objective_name}")


                y_pred = cv_data['data'][i]['y']
                y_actual = cv_data['data'][i]['x']
                min_y = cv_data['data'][0]['x'][0]
                max_y = cv_data['data'][0]['x'][1]
                iterations = np.arange(len(y_actual))  # Assuming iterations are indexed from 0 to n-1
                
                plt.figure(figsize=(6, 4))
                
                # Create a scatter plot with the 'viridis' colormap and colorbar
                norm = Normalize(vmin=0, vmax=len(iterations) - 1)
                scatter = plt.scatter(y_actual, y_pred, c=iterations, cmap=viridis, norm=norm, alpha=0.7, s=80)
                cbar = plt.colorbar(scatter, label='Iterations', orientation='vertical')
                cbar.ax.tick_params(labelsize=12)  # Increase colorbar label font size
                
                # Set the font for the colorbar label to Times New Roman
                font_properties = fm.FontProperties(family='Times New Roman', size=12)
                cbar.set_label('Iterations', fontproperties=font_properties)
                
                plt.plot([min_y, max_y], [min_y, max_y], 'k--', lw=2)
                
                plt.xlabel('Actual Values', fontname='Times New Roman', fontsize=14)
                plt.ylabel('Predicted Values', fontname='Times New Roman', fontsize=14)
                plt.title(f'Cross-validation for {self.objective_name}', fontname='Times New Roman', fontsize=15)
                
                # Set the font for x and y axis labels
                plt.xticks(fontname='Times New Roman', fontsize=12)
                plt.yticks(fontname='Times New Roman', fontsize=12)
                
                # Customize grid and ticks
                plt.grid(True, linestyle='--', alpha=0.5)
                plt.tick_params(axis='both', which='both', bottom=True, top=False, left=True, right=False)
                
                # Add a legend
                plt.legend(['Prediction point', '1:1 Line'], loc='upper left', fontsize=10)
                
                # Set the background color to white
                ax = plt.gca()
                ax.set_facecolor('white')
                
                # Adjust plot layout
                plt.tight_layout()
                
                save_location = self.pdf_crossvalidation_data_file.replace(".pdf", f"{self.objective_name}.pdf")
              
                plt.savefig(save_location, format='pdf', dpi=300, bbox_inches='tight')
                plt.close()
        
        else:
            print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Cross-validation plots generating for 1-Objective Problem")
            self.objective_name = self.first_objective_name
            print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Cross-validation plots generating for {self.objective_name}")

            y_pred = cv_data['data'][i]['y']
            y_actual = cv_data['data'][i]['x']
            min_y = cv_data['data'][0]['x'][0]
            max_y = cv_data['data'][0]['x'][1]
            iterations = np.arange(len(y_actual))  # Assuming iterations are indexed from 0 to n-1
            
            plt.figure(figsize=(6, 4))
            
            # Create a scatter plot with the 'viridis' colormap and colorbar
            norm = Normalize(vmin=0, vmax=len(iterations) - 1)
            scatter = plt.scatter(y_actual, y_pred, c=iterations, cmap=viridis, norm=norm, alpha=0.7, s=80)
            cbar = plt.colorbar(scatter, label='Iterations', orientation='vertical')
            cbar.ax.tick_params(labelsize=12)  # Increase colorbar label font size
            
            # Set the font for the colorbar label to Times New Roman
            font_properties = fm.FontProperties(family='Times New Roman', size=12)
            cbar.set_label('Iterations', fontproperties=font_properties)
            
            plt.plot([min_y, max_y], [min_y, max_y], 'k--', lw=2)
            
            plt.xlabel('Actual Values', fontname='Times New Roman', fontsize=14)
            plt.ylabel('Predicted Values', fontname='Times New Roman', fontsize=14)
            plt.title(f'Cross-validation for {self.objective_name}', fontname='Times New Roman', fontsize=15)
            
            # Set the font for x and y axis labels
            plt.xticks(fontname='Times New Roman', fontsize=12)
            plt.yticks(fontname='Times New Roman', fontsize=12)
            
            # Customize grid and ticks
            plt.grid(True, linestyle='--', alpha=0.5)
            plt.tick_params(axis='both', which='both', bottom=True, top=False, left=True, right=False)
            
            # Add a legend
            plt.legend(['Prediction point', '1:1 Line'], loc='upper left', fontsize=10)
            
            # Set the background color to white
            ax = plt.gca()
            ax.set_facecolor('white')
            
            # Adjust plot layout
            plt.tight_layout()
            
            save_location = self.pdf_crossvalidation_data_file.replace(".pdf", f"{self.objective_name}.pdf")
          
            plt.savefig(save_location, format='pdf', dpi=300, bbox_inches='tight')
            plt.close()
            print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Cross-validation plots generation complete for {self.objective_name}")


        
        return print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Cross-validation plots generated and saved succesfully")

        
        
    def model_belief(self):
        print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Generating Model-belief Plots....")

        with open(self.json_crossvalidation_data_file, 'r') as json_cv_belief_file:
            data_cv_belief = json.load(json_cv_belief_file)
            
            
        if self.second_objective_name is not None and self.third_objective_name is None:
            print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Model-belief plots generating for 2-Objective Problem")

            for i in [1, 3]:
                
                if i == 1:
                    self.objective_name = self.first_objective_name
                    print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Model-belief plots generating for {self.objective_name}")

                if i == 3:
                    self.objective_name = self.second_objective_name
                    print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Model-belief plots generating for {self.objective_name}")


                # Define a font with Times New Roman family
                times_new_roman_font = fm.FontProperties(family='Times New Roman')

                # Set font properties globally for axis numbers
                plt.rc('font', family='Times New Roman', size=14)


                predicted_values = data_cv_belief['data'][i]['y']
                actual_values = data_cv_belief['data'][i]['x']
                
                confidence_interval = 1.96 * np.std(predicted_values) / np.sqrt(len(predicted_values))
                iterations = np.arange(1, len(actual_values) + 1)
                
                plt.figure(figsize=(8, 4))
                
                # Plot actual values with markers and lines
                plt.plot(iterations, actual_values, label="Actual Values", marker='o', markersize=8, color='#1f77b4', linestyle='-', linewidth=2)
                
                # Fill the 95% confidence interval
                plt.fill_between(iterations, np.array(predicted_values) - confidence_interval, np.array(predicted_values) + confidence_interval, color='#d62728', alpha=0.5, label="95% Confidence Interval")
                
                # Set the y-axis limit to ensure the plot starts from the minimum value of actual_values
                plt.ylim(min(actual_values) - confidence_interval, max(predicted_values) + confidence_interval)
                
                # Set axis labels and title with Times New Roman font
                plt.xlabel("Trial", fontproperties=times_new_roman_font, fontsize=18)
                plt.ylabel(f"{self.objective_name}", fontproperties=times_new_roman_font, fontsize=18)
                plt.title(f'Model Belief for {self.objective_name}', fontproperties=times_new_roman_font, fontsize=20)
                
                # Customize legend and set font to Times New Roman
                legend = plt.legend(prop=times_new_roman_font, fontsize=12)
                
                # Customize grid and ticks
                plt.grid(True, linestyle='--', alpha=0.5)
                plt.tick_params(axis='both', which='both', bottom=True, top=False, left=True, right=False)
                
                # Set the background color to white
                ax = plt.gca()
                ax.set_facecolor('white')
                
                # Adjust plot layout
                plt.tight_layout()
                
                save_fig_pdf = self.pdf_modelbelief_file.replace(".pdf", f"{self.objective_name}.pdf")
                plt.savefig(save_fig_pdf, format='pdf', dpi=300, bbox_inches='tight')

                plt.close()
                print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Model-belief plots generation complete for {self.objective_name}")

                
        if self.third_objective_name is not None and self.second_objective_name is not None:
            print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Model-belief plots generating for 3-Objective Problem")

            for i in [1, 3, 5]:
                
                if i == 1:
                    self.objective_name = self.first_objective_name
                    print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Model-belief plots generating for {self.objective_name}")

                if i == 3:
                    self.objective_name = self.second_objective_name
                    print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Model-belief plots generating for {self.objective_name}")

                if i == 5:
                    self.objective_name = self.third_objective_name
                    print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Model-belief plots generating for {self.objective_name}")


                # Define a font with Times New Roman family
                times_new_roman_font = fm.FontProperties(family='Times New Roman')

                # Set font properties globally for axis numbers
                plt.rc('font', family='Times New Roman', size=14)


                predicted_values = data_cv_belief['data'][i]['y']
                actual_values = data_cv_belief['data'][i]['x']
                
                confidence_interval = 1.96 * np.std(predicted_values) / np.sqrt(len(predicted_values))
                iterations = np.arange(1, len(actual_values) + 1)
                
                plt.figure(figsize=(8, 4))
                
                # Plot actual values with markers and lines
                plt.plot(iterations, actual_values, label="Actual Values", marker='o', markersize=8, color='#1f77b4', linestyle='-', linewidth=2)
                
                # Fill the 95% confidence interval
                plt.fill_between(iterations, np.array(predicted_values) - confidence_interval, np.array(predicted_values) + confidence_interval, color='#d62728', alpha=0.5, label="95% Confidence Interval")
                
                # Set the y-axis limit to ensure the plot starts from the minimum value of actual_values
                plt.ylim(min(actual_values) - confidence_interval, max(predicted_values) + confidence_interval)
                
                # Set axis labels and title with Times New Roman font
                plt.xlabel("Trial", fontproperties=times_new_roman_font, fontsize=18)
                plt.ylabel(f"{self.objective_name}", fontproperties=times_new_roman_font, fontsize=18)
                plt.title(f'Model Belief for {self.objective_name}', fontproperties=times_new_roman_font, fontsize=20)
                
                # Customize legend and set font to Times New Roman
                legend = plt.legend(prop=times_new_roman_font, fontsize=12)
                
                # Customize grid and ticks
                plt.grid(True, linestyle='--', alpha=0.5)
                plt.tick_params(axis='both', which='both', bottom=True, top=False, left=True, right=False)
                
                # Set the background color to white
                ax = plt.gca()
                ax.set_facecolor('white')
                
                # Adjust plot layout
                plt.tight_layout()
                
                save_fig_pdf = self.pdf_modelbelief_file.replace(".pdf", f"{self.objective_name}.pdf")
                plt.savefig(save_fig_pdf, format='pdf', dpi=300, bbox_inches='tight')

                plt.close()
                print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Model-belief plots generation complete for {self.objective_name}")

        
        else:
            print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Model-belief plots generating for 1-Objective Problem")

            self.objective_name = self.first_objective_name
            print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Model-belief plots generating for {self.objective_name}")

            # Define a font with Times New Roman family
            times_new_roman_font = fm.FontProperties(family='Times New Roman')

            # Set font properties globally for axis numbers
            plt.rc('font', family='Times New Roman', size=14)


            predicted_values = data_cv_belief['data'][i]['y']
            actual_values = data_cv_belief['data'][i]['x']
            
            confidence_interval = 1.96 * np.std(predicted_values) / np.sqrt(len(predicted_values))
            iterations = np.arange(1, len(actual_values) + 1)
            
            plt.figure(figsize=(8, 4))
            
            # Plot actual values with markers and lines
            plt.plot(iterations, actual_values, label="Actual Values", marker='o', markersize=8, color='#1f77b4', linestyle='-', linewidth=2)
            
            # Fill the 95% confidence interval
            plt.fill_between(iterations, np.array(predicted_values) - confidence_interval, np.array(predicted_values) + confidence_interval, color='#d62728', alpha=0.5, label="95% Confidence Interval")
            
            # Set the y-axis limit to ensure the plot starts from the minimum value of actual_values
            plt.ylim(min(actual_values) - confidence_interval, max(predicted_values) + confidence_interval)
            
            # Set axis labels and title with Times New Roman font
            plt.xlabel("Trial", fontproperties=times_new_roman_font, fontsize=18)
            plt.ylabel(f"{self.objective_name}", fontproperties=times_new_roman_font, fontsize=18)
            plt.title(f'Model Belief for {self.objective_name}', fontproperties=times_new_roman_font, fontsize=20)
            
            # Customize legend and set font to Times New Roman
            legend = plt.legend(prop=times_new_roman_font, fontsize=12)
            
            # Customize grid and ticks
            plt.grid(True, linestyle='--', alpha=0.5)
            plt.tick_params(axis='both', which='both', bottom=True, top=False, left=True, right=False)
            
            # Set the background color to white
            ax = plt.gca()
            ax.set_facecolor('white')
            
            # Adjust plot layout
            plt.tight_layout()
            
            save_fig_pdf = self.pdf_modelbelief_file.replace(".pdf", f"{self.objective_name}.pdf")
            plt.savefig(save_fig_pdf, format='pdf', dpi=300, bbox_inches='tight')

            plt.close()
            print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Model-belief plots generation complete for {self.objective_name}")
        
        return print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Model-belief plots generated and saved succesfully")


    def model_belief_zoomed(self):
        print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Generating Model-belief Zoomed Plots....")

         
        with open(self.json_crossvalidation_data_file, 'r') as json_cv_belief_file:
            data_cv_belief = json.load(json_cv_belief_file)
            
            
        if self.second_objective_name is not None and self.third_objective_name is None:
            print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Model-belief zoomed plots generating for 2-Objective Problem")

            for i in [1, 3]:
                
                if i == 1:
                    self.objective_name = self.first_objective_name
                    print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Model-belief zoomed plots generating for {self.objective_name}")

                if i == 3:
                    self.objective_name = self.second_objective_name
                    print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Model-belief zoomed plots generating for {self.objective_name}")


                # Define a font with Times New Roman family
                times_new_roman_font = fm.FontProperties(family='Times New Roman')

                # Set font properties globally for axis numbers
                plt.rc('font', family='Times New Roman', size=14)


                predicted_values = data_cv_belief['data'][i]['y']
                actual_values = data_cv_belief['data'][i]['x']
                
                confidence_interval = 1.96 * np.std(predicted_values) / np.sqrt(len(predicted_values))
                iterations = np.arange(1, len(actual_values) + 1)
                
                plt.figure(figsize=(8, 4))
                
                # Plot actual values with markers and lines
                plt.plot(iterations, actual_values, label="Actual Values", marker='o', markersize=8, color='#1f77b4', linestyle='-', linewidth=2)
                
                # Fill the 95% confidence interval
                plt.fill_between(iterations, np.array(predicted_values) - confidence_interval, np.array(predicted_values) + confidence_interval, color='#d62728', alpha=0.5, label="95% Confidence Interval")
                
                # Set the y-axis limit to ensure the plot starts from the minimum value of actual_values
                plt.ylim(min(actual_values) - confidence_interval, max(predicted_values) + confidence_interval)
                
                # Set axis labels and title with Times New Roman font
                plt.xlabel("Trial", fontproperties=times_new_roman_font, fontsize=18)
                plt.ylabel(f"{self.objective_name}", fontproperties=times_new_roman_font, fontsize=18)
                plt.title(f'Model Belief for {self.objective_name}', fontproperties=times_new_roman_font, fontsize=20)
                
                # Customize legend and set font to Times New Roman
                legend = plt.legend(prop=times_new_roman_font, fontsize=12)
                
                # Customize grid and ticks
                plt.grid(False, linestyle='--', alpha=0.5)
                plt.tick_params(axis='both', which='both', bottom=True, top=False, left=True, right=False)
                
                # Set the background color to white
                ax = plt.gca()
                ax.set_facecolor('white')
                
                # Adjust plot layout
                plt.tight_layout()
                
                save_fig_pdf = self.pdf_modelbelief_file.replace(".pdf", f"{self.objective_name}.pdf")
                plt.savefig(save_fig_pdf, format='pdf', dpi=300, bbox_inches='tight')

                plt.close()
                print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Model-belief zoomed plots generation complete for {self.objective_name}")

                
        if self.third_objective_name is not None and self.second_objective_name is not None:
            print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Model-belief zoomed plots generating for 3-Objective Problem")

            for i in [1, 3, 5]:
                
                if i == 1:
                    self.objective_name = self.first_objective_name
                    print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Model-belief zoomed plots generating for {self.objective_name}")

                if i == 3:
                    self.objective_name = self.second_objective_name
                    print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Model-belief zoomed plots generating for {self.objective_name}")

                if i == 5:
                    self.objective_name = self.third_objective_name
                    print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Model-belief zoomed plots generating for {self.objective_name}")


                # Define a font with Times New Roman family
                times_new_roman_font = fm.FontProperties(family='Times New Roman')

                # Set font properties globally for axis numbers
                plt.rc('font', family='Times New Roman', size=14)


                predicted_values = data_cv_belief['data'][i]['y']
                actual_values = data_cv_belief['data'][i]['x']
                
                confidence_interval = 1.96 * np.std(predicted_values) / np.sqrt(len(predicted_values))
                iterations = np.arange(1, len(actual_values) + 1)
                
                plt.figure(figsize=(8, 4))
                
                # Plot actual values with markers and lines
                plt.plot(iterations, actual_values, label="Actual Values", marker='o', markersize=8, color='#1f77b4', linestyle='-', linewidth=2)
                
                # Fill the 95% confidence interval
                plt.fill_between(iterations, np.array(predicted_values) - confidence_interval, np.array(predicted_values) + confidence_interval, color='#d62728', alpha=0.5, label="95% Confidence Interval")
                
                # Set the y-axis limit to ensure the plot starts from the minimum value of actual_values
                plt.ylim(min(actual_values) - confidence_interval, max(predicted_values) + confidence_interval)
                
                # Set axis labels and title with Times New Roman font
                plt.xlabel("Trial", fontproperties=times_new_roman_font, fontsize=18)
                plt.ylabel(f"{self.objective_name}", fontproperties=times_new_roman_font, fontsize=18)
                plt.title(f'Model Belief for {self.objective_name}', fontproperties=times_new_roman_font, fontsize=20)
                
                # Customize legend and set font to Times New Roman
                legend = plt.legend(prop=times_new_roman_font, fontsize=12)
                
                # Customize grid and ticks
                plt.grid(False, linestyle='--', alpha=0.5)
                plt.tick_params(axis='both', which='both', bottom=True, top=False, left=True, right=False)
                
                # Set the background color to white
                ax = plt.gca()
                ax.set_facecolor('white')
                
                # Adjust plot layout
                plt.tight_layout()
                
                save_fig_pdf = self.pdf_modelbelief_file.replace(".pdf", f"{self.objective_name}.pdf")
                plt.savefig(save_fig_pdf, format='pdf', dpi=300, bbox_inches='tight')

                plt.close()
                print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Model-belief zoomed plots generation complete for {self.objective_name}")

        else:
            print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Model-belief zoomed plots generating for 1-Objective Problem")

            self.objective_name = self.first_objective_name
            print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Model-belief zoomed plots generating for {self.objective_name}")

            # Define a font with Times New Roman family
            times_new_roman_font = fm.FontProperties(family='Times New Roman')

            # Set font properties globally for axis numbers
            plt.rc('font', family='Times New Roman', size=14)


            predicted_values = data_cv_belief['data'][i]['y']
            actual_values = data_cv_belief['data'][i]['x']
            
            confidence_interval = 1.96 * np.std(predicted_values) / np.sqrt(len(predicted_values))
            iterations = np.arange(1, len(actual_values) + 1)
            
            plt.figure(figsize=(8, 4))
            
            # Plot actual values with markers and lines
            plt.plot(iterations, actual_values, label="Actual Values", marker='o', markersize=8, color='#1f77b4', linestyle='-', linewidth=2)
            
            # Fill the 95% confidence interval
            plt.fill_between(iterations, np.array(predicted_values) - confidence_interval, np.array(predicted_values) + confidence_interval, color='#d62728', alpha=0.5, label="95% Confidence Interval")
            
            # Set the y-axis limit to ensure the plot starts from the minimum value of actual_values
            plt.ylim(min(actual_values) - confidence_interval, max(predicted_values) + confidence_interval)
            
            # Set axis labels and title with Times New Roman font
            plt.xlabel("Trial", fontproperties=times_new_roman_font, fontsize=18)
            plt.ylabel(f"{self.objective_name}", fontproperties=times_new_roman_font, fontsize=18)
            plt.title(f'Model Belief for {self.objective_name}', fontproperties=times_new_roman_font, fontsize=20)
            
            # Customize legend and set font to Times New Roman
            legend = plt.legend(prop=times_new_roman_font, fontsize=12)
            
            # Customize grid and ticks
            plt.grid(False, linestyle='--', alpha=0.5)
            plt.tick_params(axis='both', which='both', bottom=True, top=False, left=True, right=False)
            
            # Set the background color to white
            ax = plt.gca()
            ax.set_facecolor('white')
            
            # Adjust plot layout
            plt.tight_layout()
            
            save_fig_pdf = self.pdf_modelbelief_file.replace(".pdf", f"{self.objective_name}.pdf")
            plt.savefig(save_fig_pdf, format='pdf', dpi=300, bbox_inches='tight')

            plt.close()
            print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Model-belief zoomed plots generation complete for {self.objective_name}")
       
        return print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Model-belief zoomed plots generated and saved succesfully")

         
        
    def surfaceresponse_plotter(self):
        print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Generating Surface-Response Plots....")

        
        if self.second_objective_name is not None and self.third_objective_name is None:
            print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Surface-response plots generating for 2-Objective Problem")

            for i in [1, 3]:
                
                if i == 1:
                    self.objective_name = self.first_objective_name
                    print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Surface-response plots generating for {self.objective_name}")
                    plot_response_plotdata = []
                    x1_title_dummy = []
                    x2_title_dummy = []

                    x1_title = []
                    x2_title = []

                if i == 3:
                    self.objective_name = self.second_objective_name
                    print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Surface-response plots generating for {self.objective_name}")
                    plot_response_plotdata = []
                    x1_title_dummy = []
                    x2_title_dummy = []

                    x1_title = []
                    x2_title = []

                for i in range(1, self.number_of_parameters + 1):
                    if i not in self.fixed_para:
                        for j in range(i + 1, self.number_of_parameters + 1):
                            if j not in self.fixed_para:
                                plot_response = self.plot_contour(
                                    model=self.model, param_x=f"x{i}", param_y=f"x{j}", metric_name=self.objective_name)
                                plot_response_data = plot_response[0]
                
                                x1_heading = f"x{i}"
                                x2_heading = f"x{j}"
                
                                plot_response_plotdata.append(plot_response_data)
                                x1_title_dummy.append(x1_heading)
                                x2_title_dummy.append(x2_heading)
        
                for i in range(len(x1_title_dummy)):
                    p = x1_title_dummy[i]
                    q = x2_title_dummy[i]
        
                    if p in self.parameter_names and q in self.parameter_names:
                        p_para = self.parameter_names[p]
                        q_para = self.parameter_names[q]
                        x1_title.append(p_para)
                        x2_title.append(q_para)
        
                if len(plot_response_plotdata) == len(self.json_srplot_files):
                    for k in range(len(plot_response_plotdata)):
                        json_save_surface = self.json_srplot_files[k].replace(".json", f"{self.objective_name}.json")
                        with open(json_save_surface, "w") as json_file:
                            json.dump(plot_response_plotdata[k], json_file)
                        
                        pdf_save_surface = self.pdf_srplot_files[k].replace(".pdf", f"{self.objective_name}.pdf")
                        self.contourplot_edit_and_save(
                            json_save_surface, x1_title[k], x2_title[k], self.contour_plot_title, pdf_save_surface)
                        print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Surface-response plots generation complete for {self.objective_name}")

                else:

                    print(f"[ERROR {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] The size of the plot path and plot data doesn't match")

                    
                    
        if self.third_objective_name is not None and self.second_objective_name is not None:
            print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Surface-response plots generating for 3-Objective Problem")
            
            for i in [1, 3, 5]:
                
                if i == 1:
                    self.objective_name = self.first_objective_name
                    print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Surface-response plots generating for {self.objective_name}")
                    plot_response_plotdata = []
                    x1_title_dummy = []
                    x2_title_dummy = []

                    x1_title = []
                    x2_title = []

                if i == 3:
                    self.objective_name = self.second_objective_name
                    print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Surface-response plots generating for {self.objective_name}")
                    plot_response_plotdata = []
                    x1_title_dummy = []
                    x2_title_dummy = []

                    x1_title = []
                    x2_title = []

                if i == 5:
                    self.objective_name = self.third_objective_name
                    print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Surface-response plots generating for {self.objective_name}")
                    plot_response_plotdata = []
                    x1_title_dummy = []
                    x2_title_dummy = []

                    x1_title = []
                    x2_title = []

            

                for i in range(1, self.number_of_parameters + 1):
                    if i not in self.fixed_para:
                        for j in range(i + 1, self.number_of_parameters + 1):
                            if j not in self.fixed_para:
                                plot_response = self.plot_contour(
                                    model=self.model, param_x=f"x{i}", param_y=f"x{j}", metric_name=self.objective_name)
                                plot_response_data = plot_response[0]
                
                                x1_heading = f"x{i}"
                                x2_heading = f"x{j}"
                
                                plot_response_plotdata.append(plot_response_data)
                                x1_title_dummy.append(x1_heading)
                                x2_title_dummy.append(x2_heading)
             
        
                for i in range(len(x1_title_dummy)):
                    p = x1_title_dummy[i]
                    q = x2_title_dummy[i]
        
                    if p in self.parameter_names and q in self.parameter_names:
                        p_para = self.parameter_names[p]
                        q_para = self.parameter_names[q]
                        x1_title.append(p_para)
                        x2_title.append(q_para)

        
        
        
                if len(plot_response_plotdata) == len(self.json_srplot_files):
             
                    for k in range(len(plot_response_plotdata)):
                  
                        json_save_surface = self.json_srplot_files[k].replace(".json", f"{self.objective_name}.json")
                        
                        with open(json_save_surface, "w") as json_file:
                            json.dump(plot_response_plotdata[k], json_file)
                      
                        pdf_save_surface = self.pdf_srplot_files[k].replace(".pdf", f"{self.objective_name}.pdf")
                      
                        self.contourplot_edit_and_save(
                            json_save_surface, x1_title[k], x2_title[k], self.contour_plot_title, pdf_save_surface)
                     
                        print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Surface-response plots generation complete for {self.objective_name}")

                         
                else:
                    print(f"[ERROR {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] The size of the plot path and plot data doesn't match")

        else:
            plot_response_plotdata = []
            x1_title_dummy = []
            x2_title_dummy = []

            x1_title = []
            x2_title = []
            print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Surface-response plots generating for 1-Objective Problem")
            self.objective_name = self.first_objective_name
            print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Surface-response plots generating for {self.objective_name}")

            for i in range(1, self.number_of_parameters + 1):
                if i not in self.fixed_para:
                    for j in range(i + 1, self.number_of_parameters + 1):
                        if j not in self.fixed_para:
                            plot_response = self.plot_contour(
                                model=self.model, param_x=f"x{i}", param_y=f"x{j}", metric_name=self.objective_name)
                            plot_response_data = plot_response[0]
            
                            x1_heading = f"x{i}"
                            x2_heading = f"x{j}"
            
                            plot_response_plotdata.append(plot_response_data)
                            x1_title_dummy.append(x1_heading)
                            x2_title_dummy.append(x2_heading)
    
            for i in range(len(x1_title_dummy)):
                p = x1_title_dummy[i]
                q = x2_title_dummy[i]
    
                if p in self.parameter_names and q in self.parameter_names:
                    p_para = self.parameter_names[p]
                    q_para = self.parameter_names[q]
                    x1_title.append(p_para)
                    x2_title.append(q_para)
    
            if len(plot_response_plotdata) == len(self.json_srplot_files):
                for k in range(len(plot_response_plotdata)):
                    json_save_surface = self.json_srplot_files[k].replace(".json", f"{self.objective_name}.json")
                    with open(json_save_surface, "w") as json_file:
                        json.dump(plot_response_plotdata[k], json_file)
                    
                    pdf_save_surface = self.pdf_srplot_files[k].replace(".pdf", f"{self.objective_name}.pdf")
                    self.contourplot_edit_and_save(
                        json_save_surface, x1_title[k], x2_title[k], self.contour_plot_title, pdf_save_surface)
                    print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Surface-response plots generation complete for {self.objective_name}")

            else:
                    print(f"[ERROR {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] The size of the plot path and plot data doesn't match")



        return print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Surface-response plotss generated and saved succesfully")
    
    
    def pareto_frontier(self):
        print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Generating Pareto-Front Plots....")

        
        if self.second_objective_name is not None and self.third_objective_name is None:
            print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Pareto-Front plots generating for 2-Objective Problem")

            
            objectives = self.ax_client.experiment.optimization_config.objective.objectives
            
            frontier_a = compute_posterior_pareto_frontier(
                experiment=self.ax_client.experiment,
                data=self.ax_client.experiment.fetch_data(),
                primary_objective=objectives[1].metric,
                secondary_objective=objectives[0].metric,
                absolute_metrics=[self.first_objective_name, self.second_objective_name],
                num_points=25,
            )
            
            pareto_a = self.plot_pareto_frontier(frontier_a, CI_level=0.90)
            pareto_data_a = pareto_a[0]
            
            path_to_save_pareto = self.json_pareto_file.replace(".json", f"{self.second_objective_name}_{self.first_objective_name}.json")
            
            with open(path_to_save_pareto, "w") as json_pf_file:
                json.dump(pareto_data_a, json_pf_file)
            
            x_values = pareto_data_a['data'][0]['x']
            y_values = pareto_data_a['data'][0]['y']

            # Combine x and y values along with their indices
            data_with_index = [(x, y, i) for i, (x, y) in enumerate(zip(x_values, y_values))]

            # Sort the data based on x (ascending) and y (descending)
            sorted_data = sorted(data_with_index, key=lambda k: (k[0], -k[1]))

            # Extracting sorted values and their indices
            sorted_x = [data[0] for data in sorted_data]
            sorted_y = [data[1] for data in sorted_data]
            indices = [data[2] for data in sorted_data]

            # Color mapping for iterations using viridis
            norm = mcolors.Normalize(vmin=min(indices), vmax=max(indices))
            cmap = plt.cm.viridis

            # Pareto frontier calculation
            pareto_front = [sorted_data[0]]
            for pair in sorted_data[1:]:
                if pair[1] >= pareto_front[-1][1]:
                    pareto_front.append(pair)


            # Plotting with font size customization
            plt.figure(figsize=(6, 4))
            sc = plt.scatter(sorted_x, sorted_y, c=indices, cmap=cmap, norm=norm, label='Iterations')

            plt.xlabel(f"{self.first_objective_name}", fontsize=16, fontname='Times New Roman')  # X-axis label
            plt.ylabel(f"{self.second_objective_name}", fontsize=16, fontname='Times New Roman')  # Y-axis label

            # Customize title with LaTeX font and font size
            plt.title('Pareto Frontier', fontsize=18, fontname='Times New Roman')  # Set the Pareto Frontier as the title

            # Customize font size of tick labels on both axes
            plt.xticks(fontname='Times New Roman', fontsize=14)
            plt.yticks(fontname='Times New Roman', fontsize=14)


            # Customize the legend font size and font name
            legend = plt.legend(fontsize=14)
            for text in legend.get_texts():
                text.set_fontname('Times New Roman')

            colorbar = plt.colorbar(sc)
            colorbar.ax.set_ylabel('Iteration Number', fontsize=14, fontname='Times New Roman')  # Set colorbar label font properties

            # Set font name for colorbar tick labels
            for label in colorbar.ax.get_yticklabels():
                label.set_fontname('Times New Roman')
                label.set_fontsize(14)

            plt.grid(False)
            
            
            save_path = self.pdf_pareto_file.replace(".pdf", f"{self.second_objective_name}_{self.first_objective_name}.pdf")
            
            plt.savefig(save_path, dpi=300)
            plt.close()
            print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Pareto-Front plots generation complete for {self.second_objective_name} & {self.first_objective_name}")

        
        if self.second_objective_name is not None and self.third_objective_name is not None:
            print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Pareto-Front plots generating for 3-Objective Problem")

            objectives = self.ax_client.experiment.optimization_config.objective.objectives
            
            frontier_a = compute_posterior_pareto_frontier(
                experiment=self.ax_client.experiment,
                data=self.ax_client.experiment.fetch_data(),
                primary_objective=objectives[1].metric,
                secondary_objective=objectives[0].metric,
                absolute_metrics=[self.first_objective_name, self.second_objective_name],
                num_points=25,
            )
            print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Calculating posterior pareto frontier for {self.second_objective_name} & {self.first_objective_name}")

            
            frontier_b = compute_posterior_pareto_frontier(
                experiment=self.ax_client.experiment,
                data=self.ax_client.experiment.fetch_data(),
                primary_objective=objectives[2].metric,
                secondary_objective=objectives[1].metric,
                absolute_metrics=[self.second_objective_name, self.third_objective_name],
                num_points=25,
            )
            print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Calculating posterior pareto frontier for {self.third_objective_name} & {self.second_objective_name}")

            
            
            frontier_c = compute_posterior_pareto_frontier(
                experiment=self.ax_client.experiment,
                data=self.ax_client.experiment.fetch_data(),
                primary_objective=objectives[0].metric,
                secondary_objective=objectives[2].metric,
                absolute_metrics=[self.third_objective_name, self.first_objective_name],
                num_points=25,
            )
            print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Calculating posterior pareto frontier for {self.first_objective_name} & {self.third_objective_name}")

            
            pareto_a = self.plot_pareto_frontier(frontier_a, CI_level=0.90)
            pareto_b = self.plot_pareto_frontier(frontier_b, CI_level=0.90)
            pareto_c = self.plot_pareto_frontier(frontier_c, CI_level=0.90)
            
            
            pareto_data_a = pareto_a[0]
            pareto_data_b = pareto_b[0]
            pareto_data_c = pareto_c[0]
            
            path_to_save_pareto_a = self.json_pareto_file.replace(".json", f"{self.second_objective_name}_{self.first_objective_name}.json")
            path_to_save_pareto_b = self.json_pareto_file.replace(".json", f"{self.third_objective_name}_{self.second_objective_name}.json")
            path_to_save_pareto_c = self.json_pareto_file.replace(".json", f"{self.first_objective_name}_{self.third_objective_name}.json")

            with open(path_to_save_pareto_a, "w") as json_pf_file:
                json.dump(pareto_data_a, json_pf_file)
            
            with open(path_to_save_pareto_b, "w") as json_pf_file:
                json.dump(pareto_data_b, json_pf_file)
            
            with open(path_to_save_pareto_c, "w") as json_pf_file:
                json.dump(pareto_data_c, json_pf_file)
                
            for i in [0, 1, 2]:
                if i == 0:
                    pareto_data = pareto_data_a
                    y_axis_name = self.second_objective_name
                    x_axis_name = self.first_objective_name
                    print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Pareto-Front plots generating  for {self.second_objective_name} & {self.first_objective_name}")

                    
                if i == 1:
                    pareto_data = pareto_data_b
                    y_axis_name = self.third_objective_name
                    x_axis_name = self.second_objective_name
                    print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Pareto-Front plots generating  for {self.third_objective_name} & {self.second_objective_name}")
                    
                if i == 2:
                    pareto_data = pareto_data_b
                    y_axis_name = self.first_objective_name
                    x_axis_name = self.third_objective_name
                    print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Pareto-Front plots generating  for {self.first_objective_name} & {self.third_objective_name}")

                    
            
                x_values = pareto_data['data'][0]['x']
                y_values = pareto_data['data'][0]['y']
    
                # Combine x and y values along with their indices
                data_with_index = [(x, y, i) for i, (x, y) in enumerate(zip(x_values, y_values))]
    
                # Sort the data based on x (ascending) and y (descending)
                sorted_data = sorted(data_with_index, key=lambda k: (k[0], -k[1]))
    
                # Extracting sorted values and their indices
                sorted_x = [data[0] for data in sorted_data]
                sorted_y = [data[1] for data in sorted_data]
                indices = [data[2] for data in sorted_data]
    
                # Color mapping for iterations using viridis
                norm = mcolors.Normalize(vmin=min(indices), vmax=max(indices))
                cmap = plt.cm.viridis
    
                # Pareto frontier calculation
                pareto_front = [sorted_data[0]]
                for pair in sorted_data[1:]:
                    if pair[1] >= pareto_front[-1][1]:
                        pareto_front.append(pair)
    
    
                # Plotting with font size customization
                plt.figure(figsize=(6, 4))
                sc = plt.scatter(sorted_x, sorted_y, c=indices, cmap=cmap, norm=norm, label='Iterations')
    
                plt.xlabel(f"{x_axis_name}", fontsize=16, fontname='Times New Roman')  # X-axis label
                plt.ylabel(f"{y_axis_name}", fontsize=16, fontname='Times New Roman')  # Y-axis label
    
                # Customize title with LaTeX font and font size
                plt.title('Pareto Frontier', fontsize=18, fontname='Times New Roman')  # Set the Pareto Frontier as the title
    
                # Customize font size of tick labels on both axes
                plt.xticks(fontname='Times New Roman', fontsize=14)
                plt.yticks(fontname='Times New Roman', fontsize=14)
    
    
                # Customize the legend font size and font name
                legend = plt.legend(fontsize=14)
                for text in legend.get_texts():
                    text.set_fontname('Times New Roman')
    
                colorbar = plt.colorbar(sc)
                colorbar.ax.set_ylabel('Iteration Number', fontsize=14, fontname='Times New Roman')  # Set colorbar label font properties
    
                # Set font name for colorbar tick labels
                for label in colorbar.ax.get_yticklabels():
                    label.set_fontname('Times New Roman')
                    label.set_fontsize(14)
    
                plt.grid(False)
                
                
                save_path = self.pdf_pareto_file.replace(".pdf", f"{y_axis_name}_{x_axis_name}.pdf")
                
                plt.savefig(save_path, dpi=300)
                plt.close()
                print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Pareto-Front plots generation complete for {y_axis_name} & {x_axis_name}")

                
        return print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Pareto_front plots generated and saved succesfully")


    
    
    def plot_all(self):
        
        self.performance_plotter()
        self.slice_plotter()
        self.cross_validation()
        self.surfaceresponse_plotter()
        self.model_belief()
        if self.multiobjective == True:
            self.pareto_frontier()

        return print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] All plots generated and saved succesfully...")
