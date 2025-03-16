# -*- coding: utf-8 -*-
"""
Created on Sat Mar 15 00:08:10 2025

@author: BDH1RT
"""
import pandas as pd
import os
from ansys.mapdl.core import launch_mapdl

# === Configurations ===
base_path = "C:\\Users\\bdh1rt\\Desktop\\power_module\\20250310_203308_PowerModuleModel_ECTC\\Power_Module_Model_TwoObjective\\pyMAPDLnativefiles"
eval_data_folder = "C:\\Users\\bdh1rt\\Desktop\\Spyder\\APDL2\\Res_eval\\iter_1_100_combined"
os.makedirs(eval_data_folder, exist_ok=True)

# === List of iterations to skip ===
skip_list = [65]  # Add more numbers here if needed

# === Initialize empty DataFrames to collect averages ===
nlepeq_avg_all = pd.DataFrame()
seqv_avg_all = pd.DataFrame()

# === Loop through all 100 iterations ===
for i in range(1, 101):
    if i in skip_list:
        print(f"⏩ Skipping iteration {i}")
        continue

    print(f"\n=== ✅ Processing Iteration {i} ===")
    
    rst_path = os.path.join(base_path, f"PowerModuleModelOpti_iter_{i}.rst")
    db_path = os.path.join(base_path, f"PowerModuleModelOpti_iter_{i}.db")

    if not os.path.exists(rst_path) or not os.path.exists(db_path):
        print(f"⚠️  Files missing for iteration {i}, skipping.")
        continue

    mapdl = launch_mapdl(run_location="C:\\Users\\bdh1rt\\Desktop\\Spyder\\APDL3")
    mapdl.resume(db_path)
    mapdl.post1()
    mapdl.file(rst_path)

    nlepeq_dict = {}
    seqv_dict = {}

    for lstep in range(1, 68):  # Load steps 1 to 67
        print(f"Processing Load Step: {lstep}")
        mapdl.set(lstep=lstep)
        mapdl.cmsel("s", "SOLDER")
        mapdl.nsle("s")
        mapdl.etable(lab="nlepeqtable", item="nl", comp="epeq")
        mapdl.etable(lab="seqv", item="S", comp="EQV")

        nlepeq_vals = mapdl.pretab(lab1='nlepeqtable').to_list()
        seqv_vals = mapdl.pretab(lab1='seqv').to_list()

        nlepeq_dict[lstep] = [row[1] for row in nlepeq_vals]
        seqv_dict[lstep] = [row[1] for row in seqv_vals]

    mapdl.exit()

    # Convert to DataFrames
    df_nlepeq = pd.DataFrame.from_dict(nlepeq_dict, orient='index').transpose()
    df_seqv = pd.DataFrame.from_dict(seqv_dict, orient='index').transpose()

    # Compute column-wise mean (per time step)
    nlepeq_avg = df_nlepeq.mean(axis=0).to_frame(name=f"iter_{i}")
    seqv_avg = df_seqv.mean(axis=0).to_frame(name=f"iter_{i}")

    # Append to cumulative DataFrames
    nlepeq_avg_all = pd.concat([nlepeq_avg_all, nlepeq_avg], axis=1)
    seqv_avg_all = pd.concat([seqv_avg_all, seqv_avg], axis=1)

# === Transpose so rows = iterations, columns = time steps ===
nlepeq_avg_all = nlepeq_avg_all.transpose()
seqv_avg_all = seqv_avg_all.transpose()

# === Save to Excel ===
nlepeq_avg_all.to_excel(os.path.join(eval_data_folder, "NLEPEQ_1_100.xlsx"))
seqv_avg_all.to_excel(os.path.join(eval_data_folder, "SEQ_1_100.xlsx"))

print("\n✅ All Excel files saved successfully!")

