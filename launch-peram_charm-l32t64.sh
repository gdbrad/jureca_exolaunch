#!/bin/bash
conf_start=11
conf_step=10
conf_end=1991
basedir="gio-L32T96/ini-peram_charm_clover"

for i in $(seq ${conf_start} ${conf_step} ${conf_end} ); do
  j=$(printf %02d $i)

  cfg_dir="${basedir}/cnfg${j}/numvec96"
  
  if [ -d "${cfg_dir}" ]; then
    cd ${cfg_dir}
    
    echo "Starting config ${i}"
    peram="peram_96_cfg${j}.sh"
    
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
