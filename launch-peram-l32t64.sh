#!/bin/bash
conf_start=400
conf_step=50
conf_end=4000
basedir="eric-L32T64/ini-peram_clover"

for i in $(seq ${conf_start} ${conf_step} ${conf_end} ); do
  j=$(printf %02d $i)

  cfg_dir="${basedir}/cnfg${j}/numvec64"
  
  if [ -d "${cfg_dir}" ]; then
    cd ${cfg_dir}
    
    echo "Starting config ${i}"
    peram="peram_64_cfg${j}.sh"
    
    if [ -f "${peram}" ]; then
      sbatch ${peram}
    else
      echo "Shell script ${peram} not found in ${cfg_dir}"
    fi
    
    cd - > /dev/null
  else
    echo "Configuration directory ${cfg_dir} does not exist"
  fi
done
