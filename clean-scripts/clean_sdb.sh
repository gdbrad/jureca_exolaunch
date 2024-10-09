#!/bin/bash
for i in $(seq 1001 1931); do
    # Format the number with leading zeros to 4 digits
    cfg=$(printf "%04d" $i)
    # Find and delete files matching the pattern
    rm -f peram-32_cfg${cfg}.sdb
done
