#!/bin/bash
#SBATCH --account=exncmf
#SBATCH --partition=dc-cpu
#SBATCH -t 00:30:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --gres=gpu:0

export OPENBLAS_NUM_THREADS=16
export OMP_NUM_THREADS=16
export CUDA_VISIBLE_DEVICES=0,1,2,3
CODE_DIR=/p/scratch/exotichadrons/chroma-distillation
source $CODE_DIR/install-scripts/machines/env-new-jureca-gpu.sh
CHROMA_BIN=$CODE_DIR/install/chroma/bin
SDB_DIR=/p/scratch/exotichadrons/exolaunch/perams_sdb/numvec64

BASE_DIR=/p/scratch/exotichadrons/chroma-distillation/tests
log=$BASE_DIR/log.xml
in=$BASE_DIR/infile.xml
out=$BASE_DIR/out.xml
stdout=$BASE_DIR/convert_peram.stdout
#export OPTS="-geom 1 1 1 16 -gpudirect -opt-shift -opt-prop -opt-instcombine -opt-inline -cuda-ftz -clang-opt"
#jinja this 
file=res/prop.h5
if [ -f "$file" ] ; then
    rm "$file"
fi
#jinja this
# this is passing an extra arg, the sdb file to be converted,  to the modified chroma bin, 'convert_peram' 
test_peram="$CHROMA_BIN/convert_peram peram-32_cfg11.sdb"
export OPTS="-geom 1 1 1 1" #QIO does not support multi-node jobs
# echo "START  "$(date "+%Y-%m-%dT%H:%M")
srun --threads-per-core=1 -n 1 -c 1 $test_peram $OPTS -i $in -o $out -l $log > $stdout 2>&1
# echo "FINISH JOB "$(date "+%Y-%m-%dT%H:%M")
