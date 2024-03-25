import os
import zipfile
import shutil

# Function to extract ZIP files into folders based on the folder name extracted from the file name
def extract_zip_files(directory):
    # Create a dictionary to store destination directories
    dest_dirs = {}

    # Iterate through each file in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".zip"):
            # Extract the folder name before "_farsi_persian"
            folder_name = filename.split("_farsi_persian")[0].replace("-", " ").title()
            dest_dir = os.path.join(directory, folder_name)
            # Check if the directory already exists
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)
            # Extract the ZIP file into the folder
            with zipfile.ZipFile(os.path.join(directory, filename), 'r') as zip_ref:
                zip_ref.extractall(dest_dir)
            # Store the destination directory in the dictionary
            dest_dirs[folder_name] = dest_dir

    return dest_dirs

# Function to move all extracted folders to a directory named "extracted"
def move_folders_to_extracted(directory, dest_dirs):
    # Create the "extracted" directory if it doesn't exist
    extracted_dir = os.path.join(directory, "extracted")
    os.makedirs(extracted_dir, exist_ok=True)
    
    # Move all extracted folders to the "extracted" directory
    for folder_name, dest_dir in dest_dirs.items():
        shutil.move(dest_dir, extracted_dir)
    
    return extracted_dir

# Main function
def main():
    # Prompt the user to input the directory containing .zip files
    directory = input("Enter the directory containing .zip files: ")

    # Extract ZIP files into folders based on the folder name extracted from the file name
    dest_dirs = extract_zip_files(directory)
    
    # Move all extracted folders to a directory named "extracted"
    extracted_dir = move_folders_to_extracted(directory, dest_dirs)
    
    # Count the number of ZIP archives extracted and the actual number of folders created
    num_zip_archives = len(dest_dirs)
    num_folders_created = len(os.listdir(extracted_dir))
    
    # Display success message with the actual number of folders created
    print(f"{num_zip_archives} ZIP Archives extracted in {num_folders_created} folders in {extracted_dir}.")

if __name__ == "__main__":
    main()
