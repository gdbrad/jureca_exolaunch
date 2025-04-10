import os

directories = [
    "/p/scratch/exotichadrons/exolaunch/perams_sdb/numveccnfg1991"
]

for directory in directories:
    for root, dirs, files in os.walk(directory):
        for file in files:
            if 'cfg1981' in file:
                old_file_path = os.path.join(root, file)
                new_file_name = file.replace('cfg1981', 'cfg1991')
                new_file_path = os.path.join(root, new_file_name)
                os.rename(old_file_path, new_file_path)
                print(f"Renamed: {old_file_path} -> {new_file_path}")
