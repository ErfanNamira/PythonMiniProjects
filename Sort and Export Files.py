# Sort and Export Files
# Python Mini Projects
# ErfanNamira
# https://github.com/ErfanNamira/PythonMiniProjects

import os
import glob

while True:
    # Ask the user for the folder path
    folder_path = input("Enter the folder path (or type 'exit' to quit): ")

    # Check if the user wants to exit
    if folder_path.lower() == 'exit':
        break

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
    input("Press Enter to continue...")
