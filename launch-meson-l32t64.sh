#!/bin/bash
conf_start=400
conf_step=50
conf_end=4000
basedir="eric-L32T64/ini-meson"

for i in $(seq ${conf_start} ${conf_step} ${conf_end} ); do
  j=$(printf %02d $i)

  cfg_dir="${basedir}/cnfg${j}/numvec64"
  
  if [ -d "${cfg_dir}" ]; then
    cd ${cfg_dir}
    
    echo "Starting config ${i}"
    meson="meson_64_cfg${j}.sh"
    
    if [ -f "${meson}" ]; then
      sbatch ${meson}
    else
      echo "Shell script ${meson} not found in ${cfg_dir}"
    fi
    
    cd - > /dev/null
  else
    echo "Configuration directory ${cfg_dir} does not exist"
  fi
done
