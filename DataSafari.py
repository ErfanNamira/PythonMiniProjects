import os
import psutil
import sqlite3
from datetime import datetime
from tqdm import tqdm

# Function to create the 'files' table in the database
def create_files_table(conn):
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS files (
                    id INTEGER PRIMARY KEY,
                    type TEXT,
                    file_format TEXT,
                    name TEXT,
                    address TEXT,
                    size INTEGER,
                    created_date TEXT
                )''')
    conn.commit()

# Function to search hard drives completely and record everything
def search_hard_drives():
    db_name = input("Enter the name of the database to create (without extension): ")
    if not db_name.endswith('.db'):
        db_name += '.db'
    
    # Get a list of all disk partitions
    partitions = psutil.disk_partitions(all=True)
    print("Available drives:")
    for i, partition in enumerate(partitions):
        print(f"{i + 1}. {partition.device} ({partition.mountpoint})")
    
    # Prompt the user to select a drive
    while True:
        try:
            choice = int(input("Enter the number of the drive to scan: "))
            if 1 <= choice <= len(partitions):
                drive_path = partitions[choice - 1].mountpoint
                break
            else:
                print("Invalid choice. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    # Prompt the user to include subfolders
    include_subfolders = input("Include subfolders? (yes/no): ").lower() == 'yes'
    
    # Connect to the database
    conn = sqlite3.connect(db_name)
    create_files_table(conn)  # Create the 'files' table
    c = conn.cursor()
    
    # Perform the search on the selected drive
    print(f"Scanning drive: {drive_path}")
    total_files = 0
    for root, dirs, files in os.walk(drive_path):
        total_files += len(files)
    progress_bar = tqdm(total=total_files, desc="Processing files", unit="file")
    start_time = datetime.now()
    for root, dirs, files in os.walk(drive_path):
        for name in files:
            file_path = os.path.join(root, name)
            c.execute("SELECT * FROM files WHERE address=?", (file_path,))
            if not c.fetchone():
                file_format = os.path.splitext(name)[-1].lower()
                size = int(os.path.getsize(file_path) / 1024)
                created_date = None
                try:
                    created_date = datetime.fromtimestamp(os.path.getctime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
                except OSError as e:
                    pass  # Ignore error and continue
                c.execute("INSERT INTO files (type, file_format, name, address, size, created_date) VALUES (?, ?, ?, ?, ?, ?)",
                          ('file', file_format, name, file_path, size, created_date))
            progress_bar.update(1)
        if include_subfolders:
            for name in dirs:
                dir_path = os.path.join(root, name)
                c.execute("SELECT * FROM files WHERE address=?", (dir_path,))
                if not c.fetchone():
                    created_date = None
                    try:
                        created_date = datetime.fromtimestamp(os.path.getctime(dir_path)).strftime('%Y-%m-%d %H:%M:%S')
                    except OSError as e:
                        pass  # Ignore error and continue
                    c.execute("INSERT INTO files (type, name, address, created_date) VALUES (?, ?, ?, ?)",
                              ('folder', name, dir_path, created_date))
                progress_bar.update(1)
    
    progress_bar.close()
    end_time = datetime.now()
    time_elapsed = (end_time - start_time).total_seconds()
    print(f"Search completed and data recorded successfully. Database '{db_name}' created.")
    print(f"Time elapsed: {time_elapsed:.2f} seconds.")

    # Commit changes and close the connection
    conn.commit()
    conn.close()

# Function to update an existing database
def update_database():
    db_path = input("Enter the path to the database: ")
    if not os.path.exists(db_path):
        print("Database not found.")
        return
    
    # Get a list of all disk partitions
    partitions = psutil.disk_partitions(all=True)
    print("Available drives:")
    for i, partition in enumerate(partitions):
        print(f"{i + 1}. {partition.device} ({partition.mountpoint})")
    
    # Prompt the user to select drives
    while True:
        drive_choices = input("Enter the numbers of the drives to update (separated by commas): ")
        drive_numbers = [int(choice) for choice in drive_choices.split(',') if choice.isdigit()]
        if all(1 <= choice <= len(partitions) for choice in drive_numbers):
            break
        else:
            print("Invalid choice. Please enter valid numbers.")
    
    # Connect to the database
    conn = sqlite3.connect(db_path)
    create_files_table(conn)  # Create the 'files' table
    c = conn.cursor()
    
    # Prompt the user to include subfolders
    include_subfolders = input("Include subfolders? (yes/no): ").lower() == 'yes'
    
    # Define excluded file types and directories
    excluded_file_types = {'.ini', '.tmp'}
    excluded_directories = {'$RECYCLE.BIN', '$IQY2E5Z'}
    
    # Perform the update on the database
    total_files = 0
    for choice in drive_numbers:
        drive_path = partitions[choice - 1].mountpoint
        for root, dirs, files in os.walk(drive_path):
            total_files += len(files)
    progress_bar = tqdm(total=total_files, desc="Updating database", unit="file")
    start_time = datetime.now()
    for choice in drive_numbers:
        drive_path = partitions[choice - 1].mountpoint
        for root, dirs, files in os.walk(drive_path):
            for name in files:
                if os.path.splitext(name)[-1].lower() in excluded_file_types:
                    continue
                file_path = os.path.join(root, name)
                if any(excluded_dir in file_path for excluded_dir in excluded_directories):
                    continue
                c.execute("SELECT * FROM files WHERE address=?", (file_path,))
                if not c.fetchone():
                    file_format = os.path.splitext(name)[-1].lower()
                    size = int(os.path.getsize(file_path) / 1024)
                    created_date = None
                    try:
                        created_date = datetime.fromtimestamp(os.path.getctime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
                    except OSError as e:
                        pass  # Ignore error and continue
                    c.execute("INSERT INTO files (type, file_format, name, address, size, created_date) VALUES (?, ?, ?, ?, ?, ?)",
                              ('file', file_format, name, file_path, size, created_date))
                    progress_bar.update(1)
            if include_subfolders:
                for name in dirs:
                    dir_path = os.path.join(root, name)
                    if any(excluded_dir in dir_path for excluded_dir in excluded_directories):
                        continue
                    try:
                        c.execute("SELECT * FROM files WHERE address=?", (dir_path,))
                        if not c.fetchone():
                            created_date = None
                            try:
                                created_date = datetime.fromtimestamp(os.path.getctime(dir_path)).strftime('%Y-%m-%d %H:%M:%S')
                            except OSError as e:
                                pass  # Ignore error and continue
                            c.execute("INSERT INTO files (type, name, address, created_date) VALUES (?, ?, ?, ?)",
                                      ('folder', name, dir_path, created_date))
                            progress_bar.update(1)
                    except OSError as e:
                        pass  # Ignore error and continue
    
    progress_bar.close()
    end_time = datetime.now()
    time_elapsed = (end_time - start_time).total_seconds()
    print(f"Database '{db_path}' updated successfully.")
    print(f"Time elapsed: {time_elapsed:.2f} seconds.")

    # Commit changes and close the connection
    conn.commit()
    conn.close()

def main():
    print("Welcome to DataSafari!")
    while True:
        print("\nMENU:")
        print("1. Search Hard Drives")
        print("2. Update Existing Database")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")
        if choice == '1':
            search_hard_drives()
        elif choice == '2':
            update_database()
        elif choice == '3':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 3.")

if __name__ == "__main__":
    main()