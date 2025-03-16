import psutil
import os
import subprocess
import socket
import sys

def RunAPDLMagic(Mapdl, bat_path, job_name, num_processors = None):
    """
    

    Parameters
    ----------
    Mapdl : import the "Mapdl" module by typing "from ansys.mapdl.core import Mapdl"
    bat_path : str - The absolute / relative path for the ".BAT" file.
    job_name : str - The name for the APDL job
    num_processors(Optional) : int - number of CPU's to be used. Defaults to current system CPU.
    
    Returns
    -------
    None.

    """
    
    if num_processors is None:
        num_processors = psutil.cpu_count(logical=False)
    
    
    if os.path.exists(bat_path):
        print("The .BAT file is located successfully...")
        print("Continuing with GRPC server start-up... ")
        
        with open(bat_path, 'r') as file:
            bat_contents = file.read()
        
        lines = bat_contents.split('\n')
        
        value_modified = False
        
        for i in range(len(lines)):
            if '-np' in lines[i]:
    
                parts = lines[i].split()
                for j in range(len(parts)):
                    if parts[j] == '-np':
                        current_value = int(parts[j + 1])
    
                        if current_value != num_processors:
                            parts[j + 1] = str(num_processors)
                            lines[i] = ' '.join(parts)
                            value_modified = True
                        break  
    
        modified_batch_script = '\n'.join(lines)
        
        if value_modified:
            with open(bat_path, 'w') as file:
                file.write(modified_batch_script)
        
        if value_modified:
            print(f"INFO: The new current number of CPU's used is: {num_processors} CPU's")
        else:
            print(f"INFO: The CPU number remains unchanged.The script is using {num_processors} CPU")
       
        subprocess.call([bat_path], shell=True)
        
        hostname =  socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        ip = IPAddr
        mapdl = Mapdl(ip=ip, port=50052, log_file=False)
        mapdl.clear()
        
        mapdl.jobname = job_name
        
        try:
            import emoji
            smile = emoji.emojize(":face_with_hand_over_mouth:")
        except ImportError:
            smile = ":)"
        
        print(f"GRPC server successfully started. Jobname changed to {job_name}. {smile} ")
        
    else:
        try:
            import emoji
            sad = emoji.emojize(":loudly_crying_face:")
        except ImportError:
            sad = ":'("
        
        print(f"The .BAT file is not loated / does not exist. Exiting script.... {sad}")
        sys.exit()