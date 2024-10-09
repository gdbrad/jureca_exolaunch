import os

# Define the directories containing the files
directories =[ 
    "/p/scratch/exotichadrons/exolaunch/meson_sdb/numvec32",
    "/p/scratch/exotichadrons/exolaunch/meson_sdb/numvec64",
    "/p/scratch/exotichadrons/exolaunch/meson_sdb/numvec96",
    "/p/scratch/exotichadrons/exolaunch/meson_sdb/numvec128",
]
nvecs = [32,64,96,128]

# Define the range of configuration numbers to check
cfg_range = range(11, 2000, 10)

# File name patterns
sdb_pattern = "meson-{}_cfg{}.sdb"
h5_pattern = "meson-{}_cfg{}.h5"

# Lists to store missing files
missing_sdb = []
missing_h5 = []

# Iterate through the directories and configuration numbers
for nvec, directory in zip(nvecs, directories):
    for cfg in cfg_range:
        sdb_file = sdb_pattern.format(nvec, cfg)
        h5_file = h5_pattern.format(nvec, cfg)
        
        sdb_path = os.path.join(directory, sdb_file)
        h5_path = os.path.join(directory, h5_file)
        
        sdb_exists = os.path.isfile(sdb_path)
        h5_exists = os.path.isfile(h5_path)
        
        # Debugging output
        # print(f"Checking for {sdb_path}: {'Exists' if sdb_exists else 'Missing'}")
        # print(f"Checking for {h5_path}: {'Exists' if h5_exists else 'Missing'}")
        
        if not sdb_exists:
            missing_sdb.append(sdb_path)
        if not h5_exists:
            missing_h5.append(h5_path)

# Print the results
if missing_sdb:
    print("Missing SDB files:")
    for file in missing_sdb:
        print(file)
else:
    print("All SDB files are present.")

if missing_h5:
    print("Missing HDF5 files:")
    for file in missing_h5:
        print(file)
else:
    print("All HDF5 files are present.")
