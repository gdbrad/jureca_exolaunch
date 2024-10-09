#!/bin/bash

# Define the source directory containing the files
SOURCE_DIR="./perams_sdb/numvec32"  # Replace with the actual source directory path

# Define the destination directory where files will be moved
DEST_DIR="./perams_sdb/numvec32/fail"  # Replace with the actual destination directory path

# Define the date before which files should be moved (YYYY-MM-DD format)
DATE="2024-08-30"  # Replace with the desired date

# Create the destination directory if it doesn't exist
mkdir -p "$DEST_DIR"

# Find and move files modified before the specified date
find "$SOURCE_DIR" -type f -not -path "$DEST_DIR/*" -not -name ".*" -newermt "$DATE" ! -newermt "$(date -d "$DATE +1 day" +"%Y-%m-%d")" -exec mv {} "$DEST_DIR" \;

# Optional: Verify that files were moved
echo "Moved files before $DATE from $SOURCE_DIR to $DEST_DIR"
