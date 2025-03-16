import os
import shutil
from tqdm import tqdm
from datetime import datetime

class copy_delete_previous_data:
    
    def __init__(self, script_path):
        self.script_path = script_path

    def create_folder_with_timestamp_and_name(self, base_path):
        current_datetime = datetime.now()
        timestamp = current_datetime.strftime("%Y%m%d_%H%M%S")
        folder_name = f"{timestamp}_PowerModuleModel_ECTC"
        folder_path = os.path.join(base_path, folder_name)
        os.makedirs(folder_path, exist_ok=True)
        return folder_path

    def move_and_delete_folder_contents(self, source_folder, destination_folder):
        if not os.path.exists(source_folder):
            print(f"The source folder '{source_folder}' does not exist.")
            return

        if not os.listdir(source_folder):
            print(f"The source folder '{source_folder}' is empty. Nothing to do.")
            return

        os.makedirs(destination_folder, exist_ok=True)
        items = os.listdir(source_folder)

        with tqdm(total=len(items), desc="Copying") as pbar:
            for item in items:
                item_path = os.path.join(source_folder, item)
                destination_path = os.path.join(destination_folder, item)
                if os.path.isdir(item_path):
                    shutil.copytree(item_path, destination_path)
                    print(f"Copied directory '{item}' to '{destination_folder}'.")
                else:
                    shutil.copy2(item_path, destination_path)
                    print(f"Copied file '{item}' to '{destination_folder}'.")
                pbar.update(1)

        with tqdm(total=len(items), desc="Deleting") as pbar:
            for item in items:
                item_path = os.path.join(source_folder, item)
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                    print(f"Deleted directory '{item}' from '{source_folder}'.")
                else:
                    os.remove(item_path)
                    print(f"Deleted file '{item}' from '{source_folder}'.")
                pbar.update(1)

        print("Operation completed successfully.")

    def run_all(self):
        # Determine the repo root by going one level above the script directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        repo_root = os.path.abspath(os.path.join(script_dir, os.pardir))

        print(f"Repo Root Directory: {repo_root}")

        new_folder_path = self.create_folder_with_timestamp_and_name(repo_root)
        print(f"The files will be copied to the following new folder: {new_folder_path}")
        
        self.move_and_delete_folder_contents(self.script_path, new_folder_path)

### TEST #####
# source_folder = "C:\\Users\\bdh1rt\\Desktop\\power_module\\data"
# g = copy_delete_previous_data(source_folder)
# g.run_all()
