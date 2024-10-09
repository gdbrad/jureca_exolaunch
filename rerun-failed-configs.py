import os
import argparse

# Argument parser setup
parser = argparse.ArgumentParser(description="Generate and submit shell scripts for missing configs.")
parser.add_argument('--nv', type=int, required=True, help="Number of vectors (e.g., 128)")
parser.add_argument('--obs', type=str, required=True, choices=['peram', 'meson'], help="Type of observable (either 'peram' or 'meson')")

# Parse arguments
args = parser.parse_args()
numvecs = args.nv
obs = args.obs

# Generate list of configurations in the range [11, 2001] with steps of 10
configs = list(range(11, 2002, 10))

# Base directory where the files are stored
if obs == 'meson':
    base_dir = f"/p/scratch/exotichadrons/exolaunch/meson_sdb/numvec{numvecs}"
elif obs == 'peram':
    base_dir = f"/p/scratch/exotichadrons/exolaunch/perams_sdb/numvec{numvecs}/tsrc-24"

# Function to check for missing .sdb files and zero-sized files, then prompt for deletion
def check_files_and_prompt(configs, tsrc, obs):
    zero_sized_configs = []
    missing_configs = []
    small_files_configs = []

    for cfg in configs:
        if obs == 'peram':
            file_path = f"{base_dir}/peram_{numvecs}_cfg{cfg}.sdb"
        elif obs == 'meson':
            file_path = f"{base_dir}/meson-{numvecs}_cfg{cfg}.sdb"
        
        # Check if the file exists
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            
            # Check if the file is zero-sized (for both peram and meson)
            if file_size < 54611722:  # Files less than ~54MB
                print(f"Found zero-sized file: {file_path}")
                
                # Prompt the user for deletion
                delete = input(f"Do you want to delete the zero-sized file {file_path}? (y/n): ").strip().lower()
                
                if delete == 'y':
                    os.remove(file_path)
                    print(f"Deleted zero-sized file: {file_path}")
                    zero_sized_configs.append(cfg)
                else:
                    print(f"Skipping deletion of file: {file_path}")
            
            # Check if it's a meson file and less than 5.9 GB
            elif obs == 'meson' and file_size < 6243950592:  # Files less than 5.9 GB
                print(f"Found small file (less than 5.9 GB) for meson: {file_path}")
                
                # Prompt the user for deletion
                delete = input(f"Do you want to delete the small file {file_path}? (y/n): ").strip().lower()
                
                if delete == 'y':
                    os.remove(file_path)
                    print(f"Deleted small file: {file_path}")
                    small_files_configs.append(cfg)
                else:
                    print(f"Skipping deletion of file: {file_path}")
            # Check if peram file for numvecs=128 and smaller than 9 GB
            elif obs == 'peram' and numvecs == 128 and file_size < 9663676416:  # Files less than 9 GB
                print(f"Found small file (less than 9 GB) for peram with numvecs=128: {file_path}")

                # Prompt the user for deletion
                delete = input(f"Do you want to delete the small file {file_path}? (y/n): ").strip().lower()

                if delete == 'y':
                    os.remove(file_path)
                    print(f"Deleted small file: {file_path}")
                    small_files_configs.append(cfg)
                else:
                    print(f"Skipping deletion of file: {file_path}")
        else:
            # If file doesn't exist, add to missing list
            print(f"Missing file for cfg {cfg}: {file_path}")
            missing_configs.append(cfg)

    # Print missing configurations
    if missing_configs:
        print("\nThe following configuration IDs are missing their .sdb files:")
        print(", ".join(map(str, missing_configs)))
        print(len(missing_configs))
    else:
        print("\nNo missing configuration IDs.")

    return missing_configs

# Template for the shell script
if obs == 'peram':
    template = """#!/bin/bash
# template for computing perambulators with chroma in binned srun instances

#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --partition=dc-gpu
#SBATCH --gpu-bind=none
#SBATCH --account=exotichadrons
#SBATCH -t 18:00:00
#SBATCH --gres=gpu:4

export OPENBLAS_NUM_THREADS=16
export OMP_NUM_THREADS=16

CODE_DIR=/p/scratch/exotichadrons/chroma-distillation
METAQ_DIR=/p/scratch/exotichadrons/metaq
source $CODE_DIR/install-scripts/machines/env-new-jureca-gpu.sh
chroma=$CODE_DIR/install/chroma/bin/chroma

BASE_DIR=/p/scratch/exotichadrons/exolaunch
if [ ! -d "$BASE_DIR/res/log/perams" ]; then
  mkdir -p "$BASE_DIR/res/log/perams";
fi 
if [ ! -d "$BASE_DIR/res/out/perams" ]; then
  mkdir -p "$BASE_DIR/res/out/perams";
fi 

export OPTS=" -geom 1 1 1 1"
"""
else:
    template = """#!/bin/bash
# template for computing meson elementals with chroma in binned srun instances

#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --partition=dc-gpu
#SBATCH --gpu-bind=none
#SBATCH --account=exotichadrons
#SBATCH -t 14:00:00
#SBATCH --gres=gpu:4

export OPENBLAS_NUM_THREADS=16
export OMP_NUM_THREADS=16

CODE_DIR=/p/scratch/exotichadrons/chroma-distillation
METAQ_DIR=/p/scratch/exotichadrons/metaq
source $CODE_DIR/install-scripts/machines/env-new-jureca-gpu.sh
chroma=$CODE_DIR/install/chroma/bin/chroma

BASE_DIR=/p/scratch/exotichadrons/exolaunch
export OPTS=" -geom 1 1 1 1"
"""

# Function to generate shell scripts for the missing configurations list and sbatch them
def generate_shell_scripts_and_submit(missing_configs, tsrc, obs):
    group_size = 4
    script_num = 1
    for i in range(0, len(missing_configs), group_size):
        group = missing_configs[i:i + group_size]
        script_content = template
        
        for idx, cfg in enumerate(group):
            gpu_id = idx
            if obs == 'peram':
                log_line = f'log_{cfg}=$BASE_DIR/res/log/perams/perams_{cfg}_numvecs-{numvecs}.log\n'
                in_line = f'in_{cfg}=$BASE_DIR/ini-24/cnfg{cfg}/numvec{numvecs}/peram_mg_{numvecs}_cfg{cfg}.ini.xml\n'
                out_line = f'out_{cfg}=$BASE_DIR/res/out/perams/perams_{cfg}_numvecs-{numvecs}.out.xml\n'
                output_line = f'output_{cfg}="$BASE_DIR/chroma_out/binned/perams_{cfg}_numvecs-{numvecs}_tsrc{tsrc}.out"\n'
                srun_line = f'CUDA_VISIBLE_DEVICES={gpu_id} srun --exclusive -n 1 --gres=gpu:1 -c 16 $chroma $OPTS -i $in_{cfg} -o $out_{cfg} -l $log_{cfg} > $output_{cfg} 2>&1 &\n'
                sleep_line = "sleep 20\n\n" if idx < group_size - 1 else ""
            else:
                log_line = f'log_{cfg}=$BASE_DIR/res/log/meson/meson_{cfg}_numvecs-{numvecs}.log\n'
                in_line = f'in_{cfg}=$BASE_DIR/ini/cnfg{cfg}/numvec{numvecs}/meson_{numvecs}_cfg{cfg}.ini.xml\n'
                out_line = f'out_{cfg}=$BASE_DIR/res/out/meson/meson_{cfg}_numvecs-{numvecs}.out.xml\n'
                output_line = f'output_{cfg}="$BASE_DIR/chroma_out/binned/meson/meson_{cfg}_numvecs-{numvecs}_relaunch.out"\n'
                srun_line = f'CUDA_VISIBLE_DEVICES={gpu_id} srun --exclusive -n 1 --gres=gpu:1 -c 16 $chroma $OPTS -i $in_{cfg} -o $out_{cfg} -l $log_{cfg} > $output_{cfg} 2>&1 &\n'
                sleep_line = "sleep 20\n\n" if idx < group_size - 1 else ""
            
            script_content += log_line + in_line + out_line + output_line + srun_line + sleep_line
        
        script_content += "wait\n"
        
        script_filename = f'rerun_{obs}_{numvecs}_tsrc{tsrc}_{script_num}.sh'
        with open(script_filename, 'w') as f:
            f.write(script_content)

        # Automatically submit the script using sbatch
        os.system(f"sbatch {script_filename}")

        script_num += 1

# Check for zero-sized and missing files, and prompt the user
missing_configs = check_files_and_prompt(configs, tsrc=24, obs=obs)

# Generate the shell scripts and submit them based on the missing configurations
if missing_configs:
    generate_shell_scripts_and_submit(missing_configs, tsrc=24, obs=obs)
else:
    print("No shell scripts generated as no configurations are missing.")
