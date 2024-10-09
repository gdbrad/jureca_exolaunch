#!/bin/bash

SDB_DIRS=(
    /p/scratch/exotichadrons/exolaunch/perams_sdb/numvec32
    # /p/scratch/exotichadrons/exolaunch/perams_sdb/numvec64
    # /p/scratch/exotichadrons/exolaunch/perams_sdb/numvec96
    # /p/scratch/exotichadrons/exolaunch/perams_sdb/numvec128
)

BASE_DIR=/p/scratch/exotichadrons/chroma-distillation/h5_out

# Function to get minimum size based on numvecs
get_min_size() {
    local numvecs=$1
    case $numvecs in
        32) echo $((2 * 1024**3)) ;; # 2 GB
        64) echo $((9 * 1024**3)) ;; # 9 GB
        96) echo $((20 * 1024**3)) ;; # 20 GB
        128) echo $((37 * 1024**3)) ;; # 37 GB
        *) echo 0 ;;
    esac
}

# Iterate through directories and check files
for SDB_DIR in "${SDB_DIRS[@]}"; do
    for cfg in $(seq 11 10 1999); do
        sdb_file=$(printf "$SDB_DIR/peram_32_cfg${cfg}.sdb" $cfg)
        h5_file=$(printf "$BASE_DIR/peram_32_cfg${cfg}.h5" $cfg)
        
        if [ -f "$sdb_file" ]; then
            base_name=$(basename "$sdb_file" .sdb)
            numvecs=$(echo $base_name | sed -n 's/peram_\([0-9]*\)_cfg[0-9]*.*/\1/p')
            min_size=$(get_min_size $numvecs)
            sdb_size=$(stat -c%s "$sdb_file")

            if [ $sdb_size -lt $min_size ]; then
                echo "Found existing SDB file: $sdb_file (Size: $sdb_size bytes)"
                read -p "The SDB file size is less than expected. Do you want to relaunch launch_perams_${numvecs}? (y/n): " user_input
                if [ "$user_input" == "y" ]; then
                    echo "Relaunching launch_perams_${numvecs}..."
                    ./launch_perams_${numvecs}.sh
                    continue
                else
                    echo "Skipping $sdb_file..."
                    continue
                fi
            fi

            if [ ! -f "$h5_file" ]; then
                echo "Missing HDF5 file for configuration $cfg. Relaunching relaunch_sdb_to_h5.sh..."
                ./relaunch_sdb_to_h5.sh $sdb_file
                continue
            else
                h5_size=$(stat -c%s "$h5_file")
                if [ $h5_size -lt $min_size ]; then
                    echo "Found existing HDF5 file: $h5_file (Size: $h5_size bytes)"
                    read -p "The HDF5 file size is less than expected. Do you want to relaunch relaunch_sdb_to_h5.sh? (y/n): " user_input
                    if [ "$user_input" == "y" ]; then
                        echo "Relaunching relaunch_sdb_to_h5.sh..."
                        ./relaunch_sdb_to_h5.sh $sdb_file
                        continue
                    else
                        echo "Skipping $sdb_file..."
                        continue
                    fi
                fi
            fi
        else
            echo "No .sdb files found in $SDB_DIR for configuration $cfg"
        fi
    done
done

echo "FINISH JOB $(date "+%Y-%m-%dT%H:%M")"
