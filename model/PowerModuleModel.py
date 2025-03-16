from ansys.mapdl.core import launch_mapdl, Mapdl
from ansys.dpf import core as dpf
from ansys.dpf.core import mesh_scoping_factory

import socket
import matplotlib.pyplot as plt
import subprocess
import numpy as np
import sys
import psutil
import os
import time
import datetime
import shutil
import matplotlib.font_manager as fm

class PowerModuleModel:
    
    def __init__(self,height_cu_upper, height_solder, height_sic, opti_trial_count):
        self.height_top_cu = height_cu_upper
        self.height_solder = height_solder
        self.height_sic = height_sic
        self.opti_trial_count = opti_trial_count

        
    
    def CreateFileName(self):
        self.iteration = self.opti_trial_count 
        self.file_name = f"PowerModuleModelOpti_iter_{self.opti_trial_count}"
        print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] ######## Power Module Optimization Trial: {self.opti_trial_count} ########")
        
    def PyMAPDLInitializaion(self):
        
        global mapdl
        
        
        ##############################################
        ####### DIRECTORY SETUP - DON'T CHANGE #######
        ##############################################
        self.num_processors = psutil.cpu_count(logical=False)
        self.parent_dir = os.path.dirname(os.getcwd())
        self.pTC_load = os.path.join(self.parent_dir, 'load', 'pTC_Load.txt')
        # self.pTC_load = os.path.join(self.parent_dir, 'load', 'test_load.txt')
        mapdl = launch_mapdl(nproc=self.num_processors, additional_switches='-smp',jobname=self.file_name)
        mapdl.clear()

        self.pyMAPDLnativefiles_direc = os.path.join(self.parent_dir, 'data', 'Power_Module_Model_TwoObjective', 'pyMAPDLnativefiles')
        
        if not os.path.exists(self.pyMAPDLnativefiles_direc):
            os.makedirs(self.pyMAPDLnativefiles_direc)
        
            print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] pyMAPDLnativefiles directory created")
            
        self.current_working_directory = self.pyMAPDLnativefiles_direc
        mapdl.directory = self.current_working_directory
        print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] The current MAPDL working directory is: {mapdl.directory}")
        
        
        ################ Folders to save necessary data ###################### 
        
        self.modelgeometry_plots_direc = os.path.join(self.parent_dir, 'data', 'Power_Module_Model_TwoObjective', 'modelgeometry_plots')         
        self.pyMAPDLresults_plots_direc = os.path.join(self.parent_dir, 'data', 'Power_Module_Model_TwoObjective', 'pyMAPDLresults_plots')
        self.data_numpy = os.path.join(self.parent_dir, 'data', 'Power_Module_Model_TwoObjective', 'datanumpy')
        self.max_nlepeq_np = os.path.join(self.data_numpy, f"{self.file_name}_nlepeq.npy")
        self.max_seqv_np = os.path.join(self.data_numpy, f"{self.file_name}_seqv.npy")
        
        if not os.path.exists(self.modelgeometry_plots_direc):
            os.makedirs(self.modelgeometry_plots_direc)
            print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] modelgeometry_plots directory created")
        if not os.path.exists(self.pyMAPDLresults_plots_direc):
            os.makedirs(self.pyMAPDLresults_plots_direc)
            print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] pyMAPDLresults_plots directory created")
        if not os.path.exists(self.data_numpy):
            os.makedirs(self.data_numpy)
            print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] data_numpy directory created")
            
            
    def BuildGeometry(self):
        
        ######## Fixed Geometric Parameters ########
        mapdl.clear()
        mapdl.prep7()  # Enter preprocessor
        mapdl.units("SI")  # Set unit system to SI

        ### Copper Block Length and Breadth in meters ###
        self.length_top_cu = 10e-3  
        self.width_top_cu = 10e-3   

        ### Solder Block Length and Breadth in meters ###
        self.length_solder = 5e-3  
        self.width_solder = 5e-3   

        ### Silicon Chip Block Length and Breadth in meters ###
        self.width_sic = 5e-3   
        self.length_sic = 5e-3 

        ### Set the working coordinate system to global Cartesian (0)
        mapdl.csys(0)
        mapdl.wpcsys(kcn=0)  # Set the working plane coordinate system to global
        
        
        ### Construct the Copper Block ###
        mapdl.blc4(0, 0, self.length_top_cu, self.width_top_cu, self.height_top_cu)
        
        ### Define a new local coordinate system at the top of Copper block ###
        mapdl.clocal(kcn=11, kcs=0, xl=0, yl=0, zl=self.height_top_cu)
        
        ### Activate the newly defined coordinate system ###
        mapdl.csys(11)
        mapdl.wpcsys(kcn=11)
        
        ### Create the Solder block in the new local coordinate system ###
        
        mapdl.blc4(0, 0, self.length_solder, self.width_solder, self.height_solder)
        
        mapdl.csys(0)
        mapdl.wpcsys(kcn=0)
        
        
        mapdl.clocal(kcn=12, kcs=0, xl=0, yl=0, zl=self.height_top_cu+self.height_solder)
        
        
        mapdl.csys(12)
        mapdl.wpcsys(kcn=12)
        
        
        mapdl.blc4(0, 0, self.length_sic, self.width_sic, self.height_sic)
        mapdl.csys(0)
        mapdl.wpcsys(kcn=0)
        
        #mapdl.vplot(cpos = "XY", show_lines=True, background='w')
       # mapdl.vplot(cpos = "XY", show_lines=True, background='w', window_size=[1920, 1080], off_screen = False, savefig = self.modelgeometry_plots_direc + f'/{self.file_name}_geo_in XY Position_HD.png')
       # mapdl.vplot(cpos = "iso", show_lines=True, background='w', window_size=[1920, 1080], off_screen = True, savefig = self.modelgeometry_plots_direc + f'/{self.file_name}_geo_in ISO Position _HD.png')
        print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Geometry is created. Next named selections...")

    def NamedSelections(self):
        
        self.all_solid_body = mapdl.geometry.vnum  # Get volume numbers

        ### Select and create a component for the Copper block ###
        mapdl.vsel('S', vmin=self.all_solid_body[0])
        self.cu_upper = mapdl.geometry.vnum
        mapdl.cm("Top_Cu", "VOLU")
        mapdl.allsel("all")
        
        ### Select and create a component for the Solder block ###
        mapdl.vsel('S', vmin=self.all_solid_body[1]) 
        self.solder = mapdl.geometry.vnum
        mapdl.cm("Solder", "VOLU")
        mapdl.allsel("all")
        

        ### Select and create a component for the Silicon Chip block ###
        mapdl.vsel('S', vmin=self.all_solid_body[2]) 
        self.sic = mapdl.geometry.vnum
        mapdl.cm("Si_Chip", "VOLU")
        mapdl.allsel("all")
        print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Named selections defined. Next named material properties...")
        
    def MaterialProps(self):
        ######### Material Properties ##########
        mapdl.csys(0)
        mapdl.wpcsys(kcn=0)

        mapdl.prep7()
        mapdl.units('SI')


        mapdl.toffst(value=273.15)
        mapdl.tref(tref=-40)

        ##### Copper ######
        mapdl.mp(lab='DENS', mat=1, c0=8960) # Density (kg/m³)
        mapdl.mp(lab='ALPX', mat=1, c0=16.84e-06)
        mapdl.mp(lab='EX', mat=1, c0=128.81e9)
        mapdl.mp(lab='NUXY', mat=1, c0=0.35)

        ###################

        # ########## SI Chip ########
        mapdl.mp(lab='DENS', mat=2, c0=2320) # Density (kg/m³)
        mapdl.mp(lab='ALPX', mat=2, c0=2.8e-06)
        mapdl.mp(lab='EX', mat=2, c0=129.8e9)   
        mapdl.mp(lab='NUXY', mat=2, c0=0.28)


        # ########## Solder ########
        mapdl.mp(lab='DENS', mat=3, c0=8410) # Density (kg/m³)
        mapdl.mp(lab='ALPX', mat=3, c0=2.1e-05)
        mapdl.mp(lab='EX', mat=3, c0=38.7e9)
        mapdl.mp(lab='NUXY', mat=3, c0=0.35)

        mapdl.tb(lab='RATE', mat=3, ntemp=1, npts=9, tbopt='ANAND')
        mapdl.tbdata(stloc=1, c1=45.9e6, c2=7460, c3=5.87e6, c4=2, c5=0.0942, c6=9350e6)
        mapdl.tbdata(stloc=7, c1=58.3e6, c2=0.015, c3=1.5)
        
        print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Material properties is defined. Next named defining element type...")
        
        
    def ElementType(self):
        # Element Type


        self.tid_1 = 5
        self.cid_1 = 4
        self.tid_2 = 7
        self.cid_2 = 6

        mapdl.et(itype=1, ename=186)
        mapdl.keyopt(itype=1, knum=2, value=1)


        mapdl.et(itype=2, ename=186)
        mapdl.keyopt(itype=2, knum=2, value=1)


        mapdl.et(itype=3, ename=186)
        mapdl.keyopt(itype=3, knum=2, value=1)


        mapdl.r(self.tid_1)
        mapdl.r(self.cid_1)
        mapdl.et(self.tid_1,170)
        mapdl.et(self.cid_1,174)
        mapdl.keyopt(self.cid_1,8,2) # auto create asymmetric contact (from Program Controlled setting)
        mapdl.keyopt(self.cid_1,10,0) # adjust contact stiffness each NR iteration (from Program Controlled setting)
        mapdl.keyopt(self.cid_1,12,5) # bonded always
        mapdl.keyopt(self.cid_1,18,0) # small sliding turned on by application
        mapdl.keyopt(self.cid_1,2,2) # augmented Lagrange (from Program Controlled setting)
        mapdl.keyopt(self.cid_1,5,0) # on Gauss point (from Program Controlled setting)
        mapdl.keyopt(self.cid_1,4,2)
        mapdl.keyopt(self.cid_1,9,1) # ignore initial gaps/penetration
        mapdl.keyopt(self.cid_1,7,0) # No Prediction
           
        mapdl.rmodif(self.tid_1,3,10) # FKN
        mapdl.rmodif(self.tid_1,5,0) # ICONT
        mapdl.rmodif(self.tid_1,6,0) # PINB
        mapdl.rmodif(self.tid_1,10,0) # CNOF
        mapdl.rmodif(self.tid_1,12,0) # FKT
        mapdl.rmodif(self.tid_1,36,34) # WB DSID
        mapdl.rmodif(self.cid_1,3,10) # FKN
        mapdl.rmodif(self.cid_1,5,0) # ICONT
        mapdl.rmodif(self.cid_1,6,0) # PINB
        mapdl.rmodif(self.cid_1,10,0) # CNOF
        mapdl.rmodif(self.cid_1,12,0) # FKT
        mapdl.rmodif(self.cid_1,36,34) # WB DSID


        mapdl.r(self.tid_2)
        mapdl.r(self.cid_2)
        mapdl.et(self.tid_2,170)
        mapdl.et(self.cid_2,174)
        mapdl.keyopt(self.cid_2,8,2) # auto create asymmetric contact (from Program Controlled setting)
        mapdl.keyopt(self.cid_2,10,0) # adjust contact stiffness each NR iteration (from Program Controlled setting)
        mapdl.keyopt(self.cid_2,12,5) # bonded always
        mapdl.keyopt(self.cid_2,18,0) # small sliding turned on by application
        mapdl.keyopt(self.cid_2,2,2) # augmented Lagrange (from Program Controlled setting)
        mapdl.keyopt(self.cid_2,5,0) # on Gauss point (from Program Controlled setting)
        mapdl.keyopt(self.cid_2,4,2)
        mapdl.keyopt(self.cid_2,9,1) # ignore initial gaps/penetration
        mapdl.keyopt(self.cid_2,7,0) # No Prediction
           
        mapdl.rmodif(self.tid_2,3,10) # FKN
        mapdl.rmodif(self.tid_2,5,0) # ICONT
        mapdl.rmodif(self.tid_2,6,0) # PINB
        mapdl.rmodif(self.tid_2,10,0) # CNOF
        mapdl.rmodif(self.tid_2,12,0) # FKT
        mapdl.rmodif(self.tid_2,36,37) # WB DSID
        mapdl.rmodif(self.cid_2,3,10) # FKN
        mapdl.rmodif(self.cid_2,5,0) # ICONT
        mapdl.rmodif(self.cid_2,6,0) # PINB
        mapdl.rmodif(self.cid_2,10,0) # CNOF
        mapdl.rmodif(self.cid_2,12,0) # FKT
        mapdl.rmodif(self.cid_2,36,37) # WB DSID
        
        print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Element type is defined. Next meshing...")
        

    def MeshingElems(self):
        
        mapdl.esize(1.5e-4)
        
        mapdl.type(1)
        mapdl.mat(1)
        mapdl.cmsel('S', "Top_Cu", "VOLU")
        mapdl.vsweep("ALL")
        mapdl.allsel("all")
        
        mapdl.type(2)
        mapdl.mat(2)
        mapdl.cmsel('S', "Si_Chip", "VOLU")
        mapdl.vsweep("ALL")
        mapdl.allsel("all")
        
        mapdl.esize(0.5e-4)
        mapdl.type(3)
        mapdl.mat(3)
        mapdl.cmsel('S', "Solder", "VOLU")
        mapdl.vsweep("ALL")
        mapdl.allsel("all")
        
        
        mapdl.type(4)
        mapdl.real(4)
        mapdl.asel('S', vmin = 2)
        mapdl.asel('A', vmin = 8)
        mapdl.nsla('S', nkey = 1)
        mapdl.esurf() # Generates elements overlaid on the free faces of selected nodes.
        mapdl.allsel()
        
        mapdl.type(5)
        mapdl.real(4)
        mapdl.asel('S', vmin = 7)
        mapdl.asel('A', vmin = 13)
        mapdl.nsla('S', nkey = 1)
        mapdl.esurf() # Generates elements overlaid on the free faces of selected nodes.
        mapdl.allsel()
        
        print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Mesh complete. Next applying boundary conditions...")
        mapdl.eplot(cpos = "XY", off_screen = True, savefig = self.modelgeometry_plots_direc + f'/{self.file_name}_element_in XY Position_HD.png')
        mapdl.eplot(cpos = "iso", off_screen = True, savefig = self.modelgeometry_plots_direc + f'/{self.file_name}_element_in ISO Position _HD.png')
        mapdl.eplot()

    def ApplyBoundaryConditions(self):
        
        mapdl.asel('S', vmin = 5)
        mapdl.asel('A', vmin = 11)
        mapdl.asel('A', vmin = 17)
        mapdl.nsla('S', nkey = 1)
        mapdl.d("ALL", "UX", 0.0) 
        mapdl.allsel("all")

        mapdl.asel('S', vmin = 3)
        mapdl.asel('A', vmin = 9)
        mapdl.asel('A', vmin = 15)
        mapdl.nsla('S', nkey = 1)
        mapdl.d("ALL", "UY", 0.0) 
        mapdl.allsel("all")

        mapdl.asel('S','AREA', '', 14)
        mapdl.nsla(type_='S', nkey=1)
        mapdl.d("all", "UX", 0.0)
        mapdl.d("all", "UY", 0.0)
        mapdl.allsel("all")
        
        #mapdl.eplot(cpos = "XY", off_screen = True, plot_bc = True, plot_bc_legend = True, savefig = self.modelgeometry_plots_direc + f'/{self.file_name}_element_in XY Position_HD.png')
        #mapdl.eplot(cpos = "iso", off_screen = True, plot_bc = True, plot_bc_legend = True, savefig = self.modelgeometry_plots_direc + f'/{self.file_name}_element_in ISO Position _HD.png')
        
        
        print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Applied boundary conditions. Solving static structural...")
        
    
    def SolveStaticStructural(self):
        
        mapdl.upload(self.pTC_load)
        self.temp_data = np.genfromtxt(self.pTC_load, delimiter=",")
        mapdl.load_table('ptcload', self.temp_data, 'time')
        mapdl.parameters["ptcload"]
        mapdl.starstatus("ptcload")


        mapdl.vsel("S", vmin ="All")
        mapdl.eslv('S')
        mapdl.cm(cname="all bodies", entity = "ELEM")
        mapdl.allsel()

        mapdl.vsel("S", vmin =1)
        mapdl.eslv('S')
        mapdl.cm(cname="copper", entity = "ELEM")
        mapdl.allsel()

        mapdl.vsel("S", vmin =2)
        mapdl.eslv('S')
        mapdl.cm(cname="solder", entity = "ELEM")
        mapdl.allsel()

        mapdl.vsel("S", vmin =3)
        mapdl.eslv('S')
        mapdl.cm(cname="sichip", entity = "ELEM")
        mapdl.allsel()


        mapdl.slashsolu()
        mapdl.antype(antype = 0)
        mapdl.eqslv(lab='Sparse ', keepfile=1)
        mapdl.dmpoption(filetype="RST",combine="YES")


        mapdl.cmsel("S", "all bodies","ELEM")
        mapdl.nsle('S', "all")
        mapdl.run("bf,all,temp,%ptcload%")
        mapdl.allsel("all")

        mapdl.autots(key='ON')

        data = self.temp_data[:, 0]
        for value in data:
            
            print(f"Solution at time: {value}s")
            mapdl.nsubst(nsbstp=1, nsbmx=10, nsbmn=1, carry='OFF')
            mapdl.time(time=value)
            mapdl.outres(item='erase')
            mapdl.outres(item='all', freq='none')
            mapdl.outres(item='nsol', freq='all')
            mapdl.outres(item='rsol', freq='all')
            mapdl.outres(item='eangl', freq='all')
            mapdl.outres(item='etmp', freq='all')
            mapdl.outres(item='veng', freq='all')
            mapdl.outres(item='nload', freq='all')
            mapdl.outres(item='strs', freq='all')
            mapdl.outres(item='epel', freq='all')
            mapdl.outres(item='eppl', freq='all')
            mapdl.outres(item='epth', freq='all')
            mapdl.outres(item='cont', freq='all')
            mapdl.outres(item='nldat', freq='all')

            mapdl.solve()
        mapdl.finish()
        mapdl.exit()
        time.sleep(15)
            
    def SolveAll(self):
        
        self.CreateFileName()
        self.PyMAPDLInitializaion()
        self.BuildGeometry()
        self.NamedSelections()
        self.MaterialProps()
        self.ElementType()
        self.MeshingElems()
        self.ApplyBoundaryConditions()
        
        ### Solving Model ###
        start_time_solve = time.time()
        #self.SolveStaticStructural()
        end_time_solve = time.time()
        elapsed_time_solve = end_time_solve - start_time_solve
        minutes_solve = elapsed_time_solve // 60
        seconds_solve = elapsed_time_solve % 60
        print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Solving Static Structural took  - {int(minutes_solve)} minutes {int(seconds_solve)} seconds.")
        print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Next evaluating results...")
        
        
    
    def EvaluateResults(self):
        
        ### Use the Result File to retrive results ####
        result_file = os.path.join(self.current_working_directory, f"{self.file_name}.rst")
        model = dpf.Model(result_file)
        named_selection_name = "SOLDER"
        # Get the mesh-scoping for the named selection
        mesh_scoping = model.metadata.meshed_region.named_selection(named_selection_name)
        mesh_scoping = mesh_scoping_factory.elemental_scoping(mesh_scoping)

        # Define the plastic strain and stress components
        components = {
            "NLEPEQ": dpf.operators.result.accu_eqv_plastic_strain,
            "Von_Mises": dpf.operators.result.stress_von_mises,
        }

        # Dictionary to store NumPy arrays
        results_numpy = {}

        # Loop through all components and compute results
        for comp_name, comp_operator in components.items():
            print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Processing {comp_name}...")

            # Create the operator
            operator = comp_operator()

            # Connect inputs
            operator.inputs.time_scoping.connect(model.metadata.time_freq_support.time_frequencies)
            operator.inputs.mesh_scoping.connect(mesh_scoping)
            operator.inputs.data_sources.connect(model.metadata.data_sources)
            operator.inputs.requested_location.connect("Elemental")

            # Run the operator and retrieve results
            fields_container = operator.outputs.fields_container()

            # Collect all values in a list
            all_values = []

            # Process the results
            for field in fields_container:
                all_values.append(field.data)  # Store values for each time step

            # Convert the list of lists into a NumPy array (Elements x Time Steps)
            results_numpy[comp_name] = np.array(all_values).T

            print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Stored NumPy array for {comp_name}. Shape: {results_numpy[comp_name].shape}")
            

        # Dictionary to store the final computed averages
        final_averages = {}

        # Loop through each stored NumPy array
        for comp_name, data_array in results_numpy.items():
            # Step 1: Save the NumPy array
            npy_file_path = os.path.join(self.data_numpy, f"{comp_name}.npy")
            np.save(npy_file_path, data_array)
            print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] NumPy array for {comp_name} saved at: {npy_file_path}")

            # Step 2: Compute the column-wise average (average across all elements per time step)
            column_avg = np.mean(data_array, axis=0)  # Shape will be (num_time_steps,)

            # Step 3: Compute the overall average of these column-wise averages
            overall_avg = np.mean(column_avg)

            # Store the final computed average
            final_averages[comp_name] = overall_avg
            print(f"[INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] Final average for {comp_name}: {overall_avg}")
        
        avg_nlepeq = final_averages["NLEPEQ"]
        avg_seqv = final_averages["Von_Mises"]
        
        return avg_seqv, avg_nlepeq

if __name__ == '__main__':
    
    height_cu_upper = 1e-3
    height_solder = 0.04e-3
    height_sic = 0.3e-3
    opti_trial_count = 20001

    # Create an instance of the PowerModuleModel class
    power_module = PowerModuleModel(height_cu_upper, height_solder, height_sic, opti_trial_count)
    
    # Run the solution process
    power_module.SolveAll()

    # Evaluate the results
    avg_seqv, avg_nlepeq = power_module.EvaluateResults()
    
    # Print results
    print(f"Average Von Mises Stress: {avg_seqv}")
    print(f"Average NLEPEQ: {avg_nlepeq}")
    
