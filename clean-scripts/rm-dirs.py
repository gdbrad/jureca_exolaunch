import os
import shutil

base_directory = "/p/scratch/exotichadrons/exolaunch/ini-binned-24"

for root, dirs, files in os.walk(base_directory, topdown=False):  # Use topdown=False to process subdirectories first
    for directory in dirs:
        dir_path = os.path.join(root, directory)

        # Check if the directory name matches the pattern "cfgs_X-Y"
        if directory.startswith("cfgs_") and '-' in directory:
            try:
                # Extract the range and split into two numbers
                range_part = directory.split('_')[1]
                start, end = map(int, range_part.split('-'))
                print(start,end)  
                # Check if the range represents 4 configurations
                if end - start == 30:
                    # Delete the directory if the condition is met
                    print(f"Removing directory: {dir_path}")
                    shutil.rmtree(dir_path)  # Recursively remove the directory
                else:
                    print(f"Keeping directory: {dir_path}")
            except ValueError:
                print(f"Skipping directory with invalid name: {directory}")

