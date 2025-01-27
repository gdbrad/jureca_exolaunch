#!/bin/bash
# template for computing strange perambulators with chroma in binned srun instances

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
source $CODE_DIR/install-scripts/machines/env-new-jureca-gpu.sh
chroma=$CODE_DIR/install/chroma/bin/chroma

BASE_DIR=/p/scratch/exotichadrons/exolaunch
if [ ! -d "$BASE_DIR/res/log/perams_strange" ]; then
  mkdir -p "$BASE_DIR/res/log/perams_strange";
fi 
if [ ! -d "$BASE_DIR/res/out/perams_strange" ]; then
  mkdir -p "$BASE_DIR/res/out/perams_strange";
fi 

export OPTS=" -geom 1 1 1 1"
log_21=$BASE_DIR/res/log/perams_strange/perams_strange_21_numvecs-96.log
in_21=$BASE_DIR/ini-24/cnfg21/numvec96/peram_strange_mg_96_cfg21.ini.xml
out_21=$BASE_DIR/res/out/perams_strange/perams_strange_21_numvecs-96.out.xml
output_21="$BASE_DIR/chroma_out/binned/perams_strange_21_numvecs-96_tsrc24.out"
CUDA_VISIBLE_DEVICES=0 srun --exclusive -n 1 --gres=gpu:1 -c 16 $chroma $OPTS -i $in_21 -o $out_21 -l $log_21 > $output_21 2>&1 &
sleep 20

log_1271=$BASE_DIR/res/log/perams_strange/perams_strange_1271_numvecs-96.log
in_1271=$BASE_DIR/ini-24/cnfg1271/numvec96/peram_strange_mg_96_cfg1271.ini.xml
out_1271=$BASE_DIR/res/out/perams_strange/perams_strange_1271_numvecs-96.out.xml
output_1271="$BASE_DIR/chroma_out/binned/perams_strange_1271_numvecs-96_tsrc24.out"
CUDA_VISIBLE_DEVICES=1 srun --exclusive -n 1 --gres=gpu:1 -c 16 $chroma $OPTS -i $in_1271 -o $out_1271 -l $log_1271 > $output_1271 2>&1 &
wait
