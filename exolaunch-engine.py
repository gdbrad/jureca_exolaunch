import argparse
import collections
import re
import os
import glob
import subprocess
from doit import get_var, create_after

# Parsing command-line arguments
def process_args():
    parser = argparse.ArgumentParser(description='Exolaunch Engine')
    parser.add_argument('ens', type=str, help="Select ensemble short name")
    parser.add_argument('schema', type=str, help="Select schema to execute eg. clean, create, rename, launch")
    parser.add_argument('--base_dir', type=str, default='.', help='Base directory containing the configuration directories (default: current directory)')
    return parser.parse_args()

# Define global variables
configs_to_relaunch = []
conf_start = 11
conf_step = 10
conf_end = 1991
basedir = args.base_dir

def get_min_size(numvecs): 
    '''Function to get expected file size based on numvecs
    '''
    min_size_map = {
        32: 2 * 1024**3,  # 2 GB
        64: 8 * 1024**3,  # 8 GB
        96: 20 * 1024**3,  # 20 GB
        128: 34 * 1024**3,  # 34 GB
    }
    return min_size_map.get(numvecs, 0)

# Determine base_name and SDB_DIR based on the second argument
def get_base_name_and_dir(numvecs, object_type, i):
    if object_type in ["perams", "peram"]:
        base_name = f"peram_{numvecs}_cfg{i}"
        obj = "perams"
    elif object_type in ["mesons", "meson"]:
        base_name = f"meson-{numvecs}_cfg{i}"
        obj = "meson"
    else:
        raise ValueError("Invalid object type. Use 'perams', 'peram', 'mesons', or 'meson'.")

    sdb_dir = f"/p/scratch/exotichadrons/exolaunch/{obj}_sdb/numvec{numvecs}"
    return base_name, sdb_dir

# Task to check and relaunch configs
def task_check_and_relaunch():
    for i in range(conf_start, conf_end + 1, conf_step):
        yield {
            'name': f'check_relaunch_cfg_{i}',
            'actions': [(check_and_relaunch_config, [i])],
            'targets': [f"{basedir}/cnfg{i}/numvec*"],
            'clean': True,
        }

def check_and_relaunch_config(i):
    # Extract command line arguments
    numvecs = int(get_var('numvecs', None))
    object_type = get_var('object_type', None)

    if not numvecs or not object_type:
        raise ValueError("Usage: doit numvecs=<numvecs> object_type=<object_type>")

    # Get base name and SDB directory
    base_name, sdb_dir = get_base_name_and_dir(numvecs, object_type, i)
    sdb_file = f"{sdb_dir}/{base_name}.sdb"

    if not os.path.isdir(sdb_dir):
        print(f"Configuration directory {sdb_dir} does not exist")
        return

    # Check if .sdb file exists and its size
    if not os.path.isfile(sdb_file):
        print(f".sdb file {sdb_file} does not exist.")
        configs_to_relaunch.append(base_name)
        return

    min_size = get_min_size(numvecs)
    sdb_size = os.path.getsize(sdb_file)

    if sdb_size < min_size:
        print(f"Found existing SDB file: {sdb_file} (Size: {sdb_size} bytes)")
        user_input = input(f"The SDB file size is less than expected. Do you want to relaunch and delete the file {sdb_file}? (y/n): ")
        if user_input.lower() == 'y':
            os.remove(sdb_file)
            configs_to_relaunch.append(base_name)
        else:
            print(f"Skipping {sdb_file}...")

    # Placeholder for relaunch logic
    if base_name in configs_to_relaunch:
        cfg_num = i
        cfg_dir = f"{basedir}/cnfg{cfg_num}/numvec{numvecs}"

        if os.path.isdir(cfg_dir):
            print(f"Starting config {cfg_num}")
            perams_script = f"{cfg_dir}/peram_{numvecs}_cfg{cfg_num}.sh"

            if os.path.isfile(perams_script):
                subprocess.run([perams_script], shell=True)
            else:
                print(f"Shell script {perams_script} not found in {cfg_dir}")
        else:
            print(f"Configuration directory {cfg_dir} does not exist")

def task_summary():
    def print_summary():
        print("Configs to be relaunched:")
        for config in configs_to_relaunch:
            print(config)
        print(f"FINISH JOB {subprocess.run(['date', '+%Y-%m-%dT%H:%M']).stdout}")

    return {
        'actions': [print_summary],
        'verbosity': 2
    }

# Clean up the generated tasks and files
clean(["target_dir", "another_dir"])

# Parsing ensemble information
def parse_ensemble(short_tag: str):
    long_tag = {
        "a125m280": "b3.30_ms-0.057_mud-0.129_s32t64-000-0001-0400",
        "test": "b3.70_ms0.000_mud-0.022_s32t96-000",
    }
    key = long_tag[short_tag]

    pattern = (
        r"b(?P<beta>[0-9]+\.[0-9]+)"
        r"_ms(?P<ms>[0-9]+\.[0-9]{3})"
        r"_mud-(?P<mud>[0-9]+\.[0-9]{3})"
        r"_s(?P<NL>[0-9]{2})"
        r"t(?P<NT>[0-9]{2})"
        r"-(?P<P>[0-9]{3})"
    )
    
    type_map = {
        "beta": str,
        "NT": int,
        "NL": int,
        "P": str,
        "mud": str,
        "ms": str,
    }

    match = re.match(pattern, key)
    info = (
        {
            key: type_map[key](val)
            for key, val in match.groupdict().items()
            if key in type_map
        }
        if match
        else {}
    )
    return info

# Create directory structure
def task_create_dirs():
    args = process_args()
    ens_props = parse_ensemble(args.ens)
    base_dir = args.base_dir
    dirs_to_create = [
        os.path.join(base_dir, f"{args.ens}_sdb"),
        os.path.join(base_dir, f"numvec_{ens_props['NL']}")
    ]
    
    for d in dirs_to_create:
        yield {
            'name': f'create_{d}',
            'actions': [(os.makedirs, [d])],
            'targets': [d],
            'uptodate': [os.path.exists(d)]
        }

# Clean XML and shell script files
def task_clean():
    args = process_args()
    base_dir = args.base_dir
    file_type = args.schema
    if file_type not in ['eigs', 'peram', 'meson']:
        print("Invalid file type. Please specify 'eigs', 'peram', or 'meson'.")
        return

    cfg_dirs = glob.glob(os.path.join(base_dir, 'cnfg*'))
    for cfg_dir in cfg_dirs:
        nvec_dirs = glob.glob(os.path.join(cfg_dir, 'numvec*'))
        for nvec_dir in nvec_dirs:
            xml_pattern = os.path.join(nvec_dir, f'{file_type}_*.ini.xml')
            sh_pattern = os.path.join(nvec_dir, f'{file_type}_*.sh')
            
            for pattern in [xml_pattern, sh_pattern]:
                yield {
                    'name': f'clean_{pattern}',
                    'actions': [(os.remove, [f]) for f in glob.glob(pattern)],
                    'targets': [],
                    'uptodate': [lambda: not glob.glob(pattern)]
                }

# Placeholder tasks for launching and creating files
def task_launch():
    return {
        'actions': [lambda: subprocess.run(['echo', 'Launch not yet implemented'], check=True)],
    }

def task_create_files():
    return {
        'actions': [lambda: subprocess.run(['echo', 'File creation not yet implemented'], check=True)],
    }

def task_rename():
    return {
        'actions': [lambda: subprocess.run(['echo', 'Rename not yet implemented'], check=True)],
    }

def task_relaunch():
    return {
        'actions': [lambda: subprocess.run(['echo', 'Relaunch not yet implemented'], check=True)],
    }

def task_convert_to_h5():
    for numvecs in [32, 64, 96, 128]:
        for i in range(conf_start, conf_end + 1, conf_step):
            yield {
                'name': f'convert_h5_numvec{numvecs}_cfg{i}',
                'actions': [(convert_sdb_to_h5, [numvecs, i])],
                'file_dep': [f"{SDB_BASE_DIR}/meson_sdb/numvec{numvecs}/meson-{numvecs}_cfg{i}.sdb"],
                'targets': [f"{HDF5_DIR}/meson-{numvecs}_cfg{i}.h5"],
                'clean': True,
            }

# Map schemas to tasks
def task_map_schema():
    args = process_args()
    schema_map = {
        'clean': task_clean,
        'create': task_create_files,
        'rename': task_rename,
        'launch': task_launch,
        'relaunch': task_relaunch,
    }
    task_func = schema_map.get(args.schema)
    if task_func:
        return {
            'actions': [task_func],
            'verbosity': 2,
        }
    else:
        print(f"Unknown schema: {args.schema}")
        return None
