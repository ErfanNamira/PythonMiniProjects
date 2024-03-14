# PythonMiniProjects
## How to run Scripts?
1. Install Python: If you haven't already, download and install Python from the official Python website (https://www.python.org/downloads/). Make sure to add Python to your system's PATH during installation so that you can run Python scripts from the command prompt.
2. Download the raw file of desired script and run it.
### ⛱️ Sort and Export File Names
This script asks the user for the folder path, gets a list of all files in the folder, sorts the file list alphabetically, asks the user for the output TXT file name (including the .txt extension), adds the .txt extension if not provided by the user, and writes the sorted file list to the TXT file.
### 🧮 Hash Passwords
a Python program that prompts you to enter a password and then hashes it using passlib.
```
pip3 install passlib
```
### 🎥 Video Database Creator
This Python script provides a simple command-line interface for managing a video database stored in a SQLite database file. It allows users to list video files in a specified directory and save the information into a SQLite database. Users can choose whether to include subfolders when listing video files and whether to save the database with a new unique name or overwrite an existing one.
### 🧩 Video Frame Extractor
This script extracts a frame from a video file (.mkv) specified by the user at a given frame number and saves it as a PNG image in the same directory as the script. The script utilizes the OpenCV library to load the video file, read the specified frame, and save it as an image file. It prompts the user to input the video file path and the frame number to extract. After extracting and saving the frame, the script asks the user if they want to extract another frame from the same video.
```
pip install opencv-python
```
