#!/bin/bash
#SBATCH --account=exotichadrons
#SBATCH --partition=dc-gpu
#SBATCH -t 600
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --gres=gpu:1

export OPENBLAS_NUM_THREADS=16
export OMP_NUM_THREADS=16
export CUDA_VISIBLE_DEVICES=0
CODE_DIR=/p/scratch/exotichadrons/chroma-distillation
source $CODE_DIR/install-scripts/machines/env-new-jureca-gpu.sh
CHROMA_BIN=$CODE_DIR/install/chroma/bin

BASE_DIR=/p/scratch/exotichadrons/chroma-distillation/h5_out

SDB_DIRS=(
    #/p/scratch/exotichadrons/exolaunch/perams_sdb/numvec32
    /p/scratch/exotichadrons/exolaunch/perams_sdb/numvec64
    # /p/scratch/exotichadrons/exolaunch/perams_sdb/numvec128
    #/p/scratch/exotichadrons/exolaunch/perams_sdb/numvec96
)

in="$BASE_DIR/simple.ini.xml"

# Collect cfg numbers that need processing
cfgs_to_process=()

for SDB_DIR in "${SDB_DIRS[@]}"; do
    for sdb_file in "$SDB_DIR"/*.sdb; do
        if [ -f "$sdb_file" ]; then
            base_name=$(basename "$sdb_file" .sdb)
            h5_file="$SDB_DIR/${base_name}.h5"

            if [ ! -f "$h5_file" ]; then
                echo "Adding $base_name to processing list as $h5_file does not exist."
                cfgs_to_process+=("$base_name")
            else
                echo "Skipping $sdb_file as $h5_file already exists."
            fi
        else
            echo "No .sdb files found in $SDB_DIR"
        fi
    done
done

# Process the collected cfgs
for base_name in "${cfgs_to_process[@]}"; do
    sdb_file="${SDB_DIR}/${base_name}.sdb"
    log="$BASE_DIR/log/${base_name}_log.xml"
    out="$BASE_DIR/out/${base_name}_out.xml"
    stdout="$BASE_DIR/stdout/${base_name}_convert.stdout"

    export OPTS="-geom 1 1 1 1" # QIO does not support multi-node jobs

    echo "Processing $sdb_file..."
    srun --threads-per-core=1 -n 1 -c 1 $CHROMA_BIN/convert_peram $sdb_file $OPTS -i $in -o $out -l $log > $stdout 2>&1
done

echo "FINISH JOB $(date "+%Y-%m-%dT%H:%M")"
