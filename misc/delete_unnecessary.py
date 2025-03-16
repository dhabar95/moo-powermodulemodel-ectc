import os

def delete_unnecessary(os_path):
    # List of extensions to delete
    extensions_to_delete = {
        ".DSP", ".DSPmatK", ".DSPstack", ".DSPsymb", ".DSPtri", ".DSPtriU",
        ".esav", ".full", ".ldhi", ".mntr", ".r001", ".rdb", ".stat", ".txt"
    }
    
    file_list = os.listdir(os_path)
    for file_name in file_list:
        file_path = os.path.join(os_path, file_name)
        
        try:
            if os.path.isfile(file_path):
                # Check if the file name starts with "file" or "anstmp" OR has one of the specified extensions
                if file_name.startswith("file") or file_name.startswith("anstmp") or any(file_name.endswith(ext) for ext in extensions_to_delete):
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")

path = "C:\\Users\\bdh1rt\\Desktop\\power_module\\data\\Power_Module_Model_TwoObjective\\pyMAPDLnativefiles"
delete_unnecessary(path)