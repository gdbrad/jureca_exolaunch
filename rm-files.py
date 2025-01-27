import os

for root, dirs, files in os.walk("ini-binned-24"):
    path = root.split(os.sep)  # Splitting the root path is unnecessary in this case
    print((len(path) - 1) * '---', os.path.basename(root))
    for file in files:
        if 'strange' in file:
            full_path = os.path.join(root, file)  # Construct the full file path
            os.remove(full_path)  # Remove the file
            print(len(path) * '---', file)

