# Sort and Export Files
# Python Mini Projects
# ErfanNamira
# https://github.com/ErfanNamira/Python

import os
import glob

# Ask the user for the folder path
folder_path = input("Enter the folder path: ")

# Get a list of all files in the folder
file_list = glob.glob(os.path.join(folder_path, "*"))

# Sort the file list alphabetically
file_list.sort()

# Ask the user for the output TXT file name (with .txt extension)
output_file = input("Enter the TXT file name (e.g., sorted_files.txt): ")

# Add .txt extension if not provided by the user
if not output_file.endswith(".txt"):
    output_file += ".txt"

# Write the sorted file list to the TXT file
with open(output_file, "w") as f:
    for file_name in file_list:
        f.write(file_name + "\n")

print(f"List of files has been sorted and saved to {output_file}.")
