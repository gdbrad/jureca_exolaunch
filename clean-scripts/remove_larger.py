import os
import shutil

def remove_large_files(directory, size_limit_gb):
    """
    Remove all files in the specified directory that are larger than the given size limit.

    :param directory: Path to the directory to clean up
    :param size_limit_gb: Size limit in gigabytes (files larger than this will be removed)
    """
    size_limit_bytes = size_limit_gb * (1024 ** 3)  # Convert GB to bytes
    filesrem = 0

    if not os.path.isdir(directory):
        print(f"The directory {directory} does not exist.")
        return

    for root, dirs, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            try:
                file_size = os.path.getsize(file_path)
                if file_size > size_limit_bytes:
                    # os.remove(file_path)
                    filesrem += 1
                    print(filesrem)
                    print(f"Removed: {file_path}")
            except Exception as e:
                print(f"Failed to remove {file_path}: {e}")

if __name__ == "__main__":
    directory = '/p/scratch/exotichadrons/exolaunch/perams_sdb/numvec64'
    size_limit_gb = 15  # Set the size limit to 10 GB
    remove_large_files(directory, size_limit_gb)
