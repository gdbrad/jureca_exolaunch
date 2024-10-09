import os

# Define the directories containing the files
directories = [
    "/p/scratch/exotichadrons/exolaunch/perams_sdb/numveccnfg1991"
]

# Iterate through each directory
for directory in directories:
    # Walk through the directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Check if the file name contains 'cfg1981'
            if 'cfg1981' in file:
                # Construct the full file path
                old_file_path = os.path.join(root, file)
                # Replace 'cfg1981' with 'cfg1991' in the file name
                new_file_name = file.replace('cfg1981', 'cfg1991')
                # Construct the new file path
                new_file_path = os.path.join(root, new_file_name)
                # Rename the file
                os.rename(old_file_path, new_file_path)
                # Debugging output
                print(f"Renamed: {old_file_path} -> {new_file_path}")

print("Renaming complete.")

