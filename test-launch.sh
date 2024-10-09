#!/bin/bash

conf_start=10
conf_step=10
conf_end=999
base_dir="ini"

for i in $(seq ${conf_start} ${conf_step} ${conf_end}); do
  j=$(printf %02d $i)
  
  cfg_dir="${base_dir}/cnfg${j}"
  
  if [ -d "${cfg_dir}" ]; then
    cd ${cfg_dir}
    
    echo "Starting config ${i}"
    eigs="eigs_${j}.sh"
    
    if [ -f "${eigs}" ]; then
      # Replace sbatch with echo for testing
      echo "Would execute: ${eigs}"
    else
      echo "Shell script ${eigs} not found in ${cfg_dir}"
    fi
    
    cd - > /dev/null
  else
    echo "Configuration directory ${cfg_dir} does not exist"
  fi
done
