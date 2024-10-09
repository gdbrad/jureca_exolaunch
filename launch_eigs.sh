#!/bin/bash
conf_start=991
conf_step=10
conf_end=1999
basedir="ini"

for i in $(seq ${conf_start} ${conf_step} ${conf_end} ); do
  j=$(printf %02d $i)

  cfg_dir="${basedir}/cnfg${j}"
  
  if [ -d "${cfg_dir}" ]; then
    cd ${cfg_dir}
    
    echo "Starting config ${i}"
    eigs="eigs_${j}.sh"
    
    if [ -f "${eigs}" ]; then
      sbatch ${eigs}
    else
      echo "Shell script ${eigs} not found in ${cfg_dir}"
    fi
    
    cd - > /dev/null
  else
    echo "Configuration directory ${cfg_dir} does not exist"
  fi
done
