import os

def main():
    # Prompt user for directory path
    directory_path = input("Enter the directory path: ")

    # List all files in the directory and sort them by file name
    files = sorted(os.listdir(directory_path))

    # Write the sorted list of files to a .txt file
    with open('file_list.txt', 'w') as file:
        for f in files:
            file.write(f + '\n')

    # Display success message
    print("File list has been saved to file_list.txt")

    # Wait for user to press enter
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
