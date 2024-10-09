#!/bin/bash

# Directory where the files are located
numvec=128
BASE_DIR="perams_sdb/numvec128"

echo "Previewing changes for .sdb files:"
for sdb_file in "$BASE_DIR"/peram-128_cfg*.sdb; do
    if [ -f "$sdb_file" ]; then
        new_name=$(basename "$sdb_file" | sed 's/peram-128/peram_128/')
        echo "Current: $sdb_file"
        echo "Change to: $BASE_DIR/$new_name"
    fi
done

echo ""

echo "Previewing changes for .h5 files:"
for h5_file in "$BASE_DIR"/peram-128_cfg*.h5; do
    if [ -f "$h5_file" ]; then
        new_name=$(basename "$h5_file" | sed 's/peram-128/peram_128/')
        echo "Current: $h5_file"
        echo "Change to: $BASE_DIR/$new_name"
    fi
done

echo ""
read -p "Do you want to proceed with renaming? (y/n): " user_input

if [ "$user_input" == "y" ]; then
    echo "Renaming .sdb files:"
    for sdb_file in "$BASE_DIR"/peram-128_cfg*.sdb; do
        if [ -f "$sdb_file" ]; then
            new_name=$(basename "$sdb_file" | sed 's/peram-128/peram_128/')
            mv "$sdb_file" "$BASE_DIR/$new_name"
            echo "Renamed: $sdb_file to $BASE_DIR/$new_name"
        fi
    done

    echo ""

    echo "Renaming .h5 files:"
    for h5_file in "$BASE_DIR"/peram-128_cfg*.h5; do
        if [ -f "$h5_file" ]; then
            new_name=$(basename "$h5_file" | sed 's/peram-128/peram_128/')
            mv "$h5_file" "$BASE_DIR/$new_name"
            echo "Renamed: $h5_file to $BASE_DIR/$new_name"
        fi
    done
else
    echo "No changes were made."
fi

