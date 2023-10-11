## All the files that are scraped are given page's name and that is messing up
## extensions of files in OS. Hence this utility to rename them back to txt extension


import os

# Set the path to the folder containing the files
folder_path = '/Users/mounicaayalasomayajula/Desktop/DATA-298A/prompt/dataset/chhs'

# Get a list of all files in the folder
all_files = os.listdir(folder_path)

# Loop through the files
for filename in all_files:
    # Skip directories
    if os.path.isdir(os.path.join(folder_path, filename)):
        continue
    # Extract the file name and extension
    file_name, file_extension = os.path.splitext(filename)
    print(filename)
    print("\n")
    print(file_extension)

    # Construct the new filename by removing the dot from the file name and appending .txt
    new_filename = file_name.replace('.', '') + '.txt'
    print(new_filename)
    # Construct the full file paths for the old and new filenames
    old_file_path = os.path.join(folder_path, filename)
    print(old_file_path)
    new_file_path = os.path.join(folder_path, new_filename)
    print(new_file_path)
    if os.path.exists(new_file_path):
        # Append a numerical suffix to the filename
        suffix = 1
        while True:
            # Construct the new filename with the numerical suffix
            new_filename = file_name.replace('.', '') + str(suffix) + '.txt'
            new_file_path = os.path.join(folder_path, new_filename)
            # Check if the new filename with the suffix also exists
            if not os.path.exists(new_file_path):
                break
            suffix += 1
    
    # Rename the file
    os.rename(old_file_path, new_file_path)
