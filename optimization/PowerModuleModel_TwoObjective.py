### power Module Model Optimization Script - Viscoelastic Material Properties
# -----------------------------------------------------------------------------
# This script performs parameter optimization for a Power Module model using
# viscoelastic materials. It utilizes Bayesian Optimization (Ax) to minimize
# two objectives: Avg_SEQV and Avg_NLEPEQ. The simulation is executed using a
# model built in PowerModuleModel.
# -----------------------------------------------------------------------------

import sys
import os
import datetime
import traceback
import time
import numpy as np
import psutil

# Add parent directory to system path to access custom modules
sys.path.append('..')

# Ax imports for optimization
from ax.modelbridge.generation_strategy import GenerationStrategy, GenerationStep
from ax.service.ax_client import AxClient, ObjectiveProperties
from ax.modelbridge.registry import Models
from ax.plot.diagnostic import interact_cross_validation
from ax.modelbridge.cross_validation import cross_validate
from ax.plot.slice import plot_slice
from ax.plot.contour import plot_contour
from ax.plot.pareto_frontier import plot_pareto_frontier

# Custom module imports
from model.PowerModuleModel import PowerModuleModel
from misc.time_filename import time_for_filename
from plotutils.contourplot_edit_and_save import contourplot_edit_and_save
from plotutils.sliceplot_edit_and_save import sliceplot_edit_and_save
from misc.json_mean_extractor import json_mean_extractor
from plotutils.model_performance import model_performance
from misc.file_path_gen import file_path_gen
from plotutils.optimization_plotter import optimization_plotter
from misc.delete_unnecessary import delete_unnecessary
from misc.copy_delete_previous_data import copy_delete_previous_data
from misc.initial_param_MOO_2_obj import initial_param_MOO_2_obj
from misc.load_previousexp_trial_MOO import load_previousexp_trial_MOO
# from misc.send_email import send_email  # Optional: Enable email notifications on crash

# -----------------------------------------------------------------------------
# Create necessary directories and file paths for saving results
# -----------------------------------------------------------------------------
time_stamp = time_for_filename()
parent_dir = os.path.dirname(os.getcwd())

data = os.path.join(parent_dir, "data", "Power_Module_Model_TwoObjective")
trial_data_path = "ADD TRIAL DATA PATH"
data_array = os.path.join(data, "savedarraydata")
bearing_json = os.path.join(data, "bearing_json")
bearing_pdf = os.path.join(data, "bearing_pdf")

number_of_parameters = 3
objective_name = "PMM_Opti"
first_objective_name = "Avg_SEQV"
second_objective_name = "Avg_NLEPEQ"
third_objective_name = None
fixed_para_list = []

f = file_path_gen(time_stamp, bearing_json, bearing_pdf, number_of_parameters, fixed_para_list, objective_name)
(
    path_json_data, path_json_performance, path_pdf_performance,
    path_json_crossvalidation, path_pdf_crossvalidation,
    path_json_surfaceresponse, path_pdf_surfaceresponse,
    path_json_sliceplot, path_pdf_sliceplot,
    path_pdf_modelbelief, path_pdf_modelbelief_zoomed,
    path_pdf_pareto, path_json_pareto
) = f.generate_all()

# Create directories if not exist
for folder in [data, data_array, bearing_json, bearing_pdf]:
    if not os.path.exists(folder):
        os.makedirs(folder)
        print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] {os.path.basename(folder)} folder created")

# -----------------------------------------------------------------------------
# Print processor information for logging
# -----------------------------------------------------------------------------
num_processors = psutil.cpu_count(logical=False)
print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] {num_processors} physical cores available")

# -----------------------------------------------------------------------------
# Parameter and optimization settings
# -----------------------------------------------------------------------------
data_avg_SEQV_param_array = os.path.join(data_array, "avg_SEQV_param_array.npy")
data_avg_NLEPEQ_param_array = os.path.join(data_array, "avg_NLEPEQ_param_array.npy")
avg_SEQV_param_array = []
avg_NLEPEQ_param_array = []

# Optimization hyperparameters
num_trials_SOBOL = 0
num_trials_MOO = 40
total_trial_number = num_trials_SOBOL + num_trials_MOO
opti_trial_count = 66

# Parameter bounds and initial values (in meters)
param_bounds = {
    "x1": (0.5e-3, 1.5e-3, 1e-3),   # Cu thickness
    "x2": (0.01e-3, 0.09e-3, 0.04e-3),  # Solder thickness
    "x3": (0.1e-3, 0.5e-3, 0.3e-3),   # Si chip thickness
}

parameter_names = {
    "x1": "x1: Copper thickness [mm]",
    "x2": "x2: Solder thickness [mm]",
    "x3": "x3: Silicon chip thickness [mm]"
}
contour_plot_title =  "<b>Contour Plot - Power Module Model</b>"

# -----------------------------------------------------------------------------
# Objective Function for Ax optimization
# -----------------------------------------------------------------------------
def PowerModuleModel_Opti(height_cu_upper, height_solder, height_sic):
    global avg_SEQV_param_array, avg_NLEPEQ_param_array, opti_trial_count
    power_module = PowerModuleModel(height_cu_upper, height_solder, height_sic, opti_trial_count)
    power_module.SolveAll()
    avg_SEQV, avg_NLEPEQ = power_module.EvaluateResults()
    avg_SEQV_param_array.append([avg_SEQV, height_cu_upper, height_solder, height_sic])
    avg_NLEPEQ_param_array.append([avg_NLEPEQ, height_cu_upper, height_solder, height_sic])
    opti_trial_count += 1
    return avg_SEQV, avg_NLEPEQ

# Ax generation strategy: Sobol followed by Multi-objective Bayesian Optimization
gs = GenerationStrategy(steps=[
    GenerationStep(model=Models.SOBOL, num_trials=num_trials_SOBOL, min_trials_observed=1, max_parallelism=5),
    GenerationStep(model=Models.MOO, num_trials=-1, max_parallelism=3)
])

# Initialize Ax client
ax_client = AxClient(generation_strategy=gs)
ax_client.create_experiment(
    name=objective_name,
    parameters=[{
        "name": name,
        "type": "range",
        "bounds": [param_bounds[name][0], param_bounds[name][1]],
        "value_type": "float"
    } for name in ["x1", "x2", "x3"]],
    objectives={
        first_objective_name: ObjectiveProperties(minimize=True),
        second_objective_name: ObjectiveProperties(minimize=True),
    },
)

# Evaluation wrapper for Ax trial format
def PowerModuleModel_Opti_Evaluation_Function(parameterization):
    x = np.array([parameterization[f"x{i+1}"] for i in range(3)])
    multi_obj = PowerModuleModel_Opti(*x)
    return {
        first_objective_name: (multi_obj[0], 0.0),
        second_objective_name: (multi_obj[1], 0.0)
    }

# -----------------------------------------------------------------------------
# Attach initial parameters and optionally reload previous trial results
# -----------------------------------------------------------------------------
print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Attaching initial parameters ...")
initial_param_dict = {name: param_bounds[name][2] for name in ["x1", "x2", "x3"]}
init_moo = initial_param_MOO_2_obj(ax_client, PowerModuleModel_Opti, initial_param_dict, first_objective_name, second_objective_name)
init_moo.trial_initiation()

# -----------------------------------------------------------------------------
# Optimization Loop
# -----------------------------------------------------------------------------
print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Starting optimization trials ...")
start_time = time.time()

try:
    for i in range(total_trial_number):
        print(f"Trial {i}")
        delete_unnecessary(os.getcwd())
        parameters, trial_index = ax_client.get_next_trial()
        result = PowerModuleModel_Opti_Evaluation_Function(parameters)
        ax_client.complete_trial(trial_index=trial_index, raw_data=result)

        # Save progress to JSON and NumPy files
        save_path = path_json_data.replace(".json", f"upto_{trial_index}_trial.json")
        ax_client.save_to_json_file(save_path)

        np.save(data_avg_SEQV_param_array.replace(".npy", f"upto_{trial_index}_trial.npy"), avg_SEQV_param_array)
        np.save(data_avg_NLEPEQ_param_array.replace(".npy", f"upto_{trial_index}_trial.npy"), avg_NLEPEQ_param_array)

        time.sleep(10)

        # Plotting results periodically
        if i == total_trial_number - 1:
            path_json_data = save_path
        if i in [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]:
            model = ax_client.generation_strategy.model
            op = optimization_plotter(
                plot_contour, model, plot_slice, parameter_names,
                number_of_parameters, first_objective_name, contour_plot_title,
                path_json_surfaceresponse, path_pdf_surfaceresponse,
                path_json_sliceplot, path_pdf_sliceplot, path_pdf_performance,
                path_json_data, contourplot_edit_and_save, sliceplot_edit_and_save,
                model_performance, json_mean_extractor, cross_validate,
                interact_cross_validation, path_json_crossvalidation,
                path_pdf_crossvalidation, path_pdf_modelbelief,
                path_pdf_modelbelief_zoomed, trial_index, fixed_para_list,
                ax_client, path_pdf_pareto, path_json_pareto,
                second_objective_name, third_objective_name,
                plot_pareto_frontier, multiobjective=True)
            plotting_start = time.time()
            op.plot_all()
            plotting_time = time.time() - plotting_start
            print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Plotting time: {plotting_time:.1f} sec")

except Exception as e:
    error_subject = f"Simulation Error at {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}"
    error_body = f"Exception:\n{str(e)}\n\nTraceback:\n{traceback.format_exc()}"
    # send_email(error_subject, error_body)

# -----------------------------------------------------------------------------
# Final Logging
# -----------------------------------------------------------------------------
end_time = time.time()
elapsed = end_time - start_time
print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Total optimization time: {elapsed // 60:.0f} minutes {elapsed % 60:.0f} seconds")

delete_unnecessary(os.getcwd())
