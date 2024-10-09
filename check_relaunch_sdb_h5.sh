#!/bin/bash
# LOCAL_DIR="/home/grant/exolaunch"

SDB_DIRS=(
    /p/scratch/exotichadrons/exolaunch/perams_sdb/numvec32
)
conf_start=11
conf_step=10
conf_end=1991
basedir="ini"
numvecs=32
# in="$BASE_DIR/simple.ini.xml"

get_min_size() {
    local numvecs=$1
    case $numvecs in
        32) echo $((2 * 1024**3)) ;; # 2 GB
        64) echo $((9 * 1024**3)) ;; # 9 GB
        96) echo $((20 * 1024**3)) ;; # 20 GB
        128) echo $((34 * 1024**3)) ;; # 37 GB
        *) echo 0 ;;
    esac
}

for SDB_DIR in "${SDB_DIRS[@]}"; do
    for sdb_file in "$SDB_DIR"/*.sdb; do
        if [ -f "$sdb_file" ]; then
            base_name=$(basename "$sdb_file" .sdb)
            numvecs=$(echo $base_name | sed -n 's/peram_\([0-9]*\)_cfg[0-9]*.*/\1/p')

            min_size=$(get_min_size $numvecs)
            sdb_size=$(stat -c%s "$sdb_file")

            if [ $sdb_size -lt $min_size ]; then
                echo "Found existing SDB file: $sdb_file (Size: $sdb_size bytes)"

                read -p "The SDB file size is less than expected. Do you want to relaunch launch_perams_${numvecs}? (y/n): " user_input
                if [ "$user_input" == "y" ]; then
                    echo "Would relaunch "$base_name.sh"..."
                    continue
                else
                    echo "Skipping $sdb_file..."
                    continue
                fi
            fi

            # log="$BASE_DIR/log/${base_name}_log.xml"
            # out="$BASE_DIR/out/${base_name}_out.xml"
            # stdout="$BASE_DIR/stdout/${base_name}_convert.stdout"
            # file="$BASE_DIR/${base_name}.h5"

            # if [ -f "$file" ]; then
            #     h5_size=$(stat -c%s "$file")
            #     if [ $h5_size -lt $min_size ]; then
            #         echo "Found existing HDF5 file: $file (Size: $h5_size bytes)"
            #         read -p "The HDF5 file size is less than expected. Do you want to relaunch relaunch_sdb_to_h5.sh? (y/n): " user_input
            #         if [ "$user_input" == "y" ]; then
            #             echo "Would relaunch relaunch_sdb_to_h5.sh..."
            #             continue
            #         else
            #             echo "Skipping $sdb_file..."
            #             continue
            #         fi
            #     fi
            # fi

            # echo "Would process $sdb_file with the following settings:"
            # echo "Base name: $base_name"
            # echo "HDF5 file: $file"
        else
            echo "No .sdb files found in $SDB_DIR"
        fi
    done
done

echo "FINISH JOB $(date "+%Y-%m-%dT%H:%M")"
