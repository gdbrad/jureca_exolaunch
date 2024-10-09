#!/bin/bash

# Define the path where the directories are located
DIR_PATH="ini"

for dir in "${DIR_PATH}"/cnfg*/numvec*; 
do
    echo "Processing directory: $dir"
    if [[ -d $dir ]]; then
        echo "Directory exists: $dir"
        if [[ $dir =~ 0 ]]; then
            echo "Directory contains 0: $dir"
            rm -r "$dir"
        else
            echo "Directory does not contain 0: $dir"
        fi
    else
        echo "Not a directory: $dir"
    fi
done
