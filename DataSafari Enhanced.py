import os
import psutil
import sqlite3
from datetime import datetime
from tqdm import tqdm
import concurrent.futures

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

# Function to insert files into the database
def insert_files(conn, files):
    c = conn.cursor()
    c.executemany("INSERT INTO files (type, file_format, name, address, size, created_date) VALUES (?, ?, ?, ?, ?, ?)", files)
    conn.commit()

# Function to insert directories into the database
def insert_directories(conn, directories):
    c = conn.cursor()
    c.executemany("INSERT INTO files (type, name, address, created_date) VALUES (?, ?, ?, ?)", directories)
    conn.commit()

# Function to process a single file
def process_file(file_path):
    file_format = os.path.splitext(os.path.basename(file_path))[-1].lower()
    size = int(os.path.getsize(file_path) / 1024)
    created_date = None
    try:
        created_date = datetime.fromtimestamp(os.path.getctime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
    except OSError as e:
        pass  # Ignore error and continue
    return ('file', file_format, os.path.basename(file_path), file_path, size, created_date)

# Function to search hard drives completely and record everything
def search_hard_drives():
    db_name = input("Enter the name of the database to create (without extension): ")
    if not db_name.endswith('.db'):
        db_name += '.db'
    
    partitions = psutil.disk_partitions(all=True)
    print("Available drives:")
    for i, partition in enumerate(partitions):
        print(f"{i + 1}. {partition.device} ({partition.mountpoint})")
    
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
    
    include_subfolders = input("Include subfolders? (yes/no): ").lower() == 'yes'
    
    conn = sqlite3.connect(db_name)
    create_files_table(conn)
    
    print(f"Scanning drive: {drive_path}")
    total_files = 0
    for root, dirs, files in os.walk(drive_path):
        total_files += len(files)
    progress_bar = tqdm(total=total_files, desc="Processing files", unit="file")
    start_time = datetime.now()
    processed_files = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_file, os.path.join(root, name)) for root, dirs, files in os.walk(drive_path) for name in files]
        for future in concurrent.futures.as_completed(futures):
            processed_files.append(future.result())
            progress_bar.update(1)
    progress_bar.close()
    insert_files(conn, processed_files)
    end_time = datetime.now()
    time_elapsed = (end_time - start_time).total_seconds()
    print(f"Search completed and data recorded successfully. Database '{db_name}' created.")
    print(f"Time elapsed: {time_elapsed:.2f} seconds.")
    conn.close()

# Function to update the database for a single drive
def update_database_for_drive(drive_path, exclude_types, exclude_dirs):
    processed_files = []
    for root, dirs, files in os.walk(drive_path):
        for name in files:
            file_path = os.path.join(root, name)
            if os.path.splitext(name)[-1].lower() in exclude_types:
                continue
            if any(excluded_dir in file_path for excluded_dir in exclude_dirs):
                continue
            processed_files.append(process_file(file_path))
    return processed_files

# Function to update an existing database
def update_database():
    db_path = input("Enter the path to the database: ")
    if not os.path.exists(db_path):
        print("Database not found.")
        return
    
    partitions = psutil.disk_partitions(all=True)
    print("Available drives:")
    for i, partition in enumerate(partitions):
        print(f"{i + 1}. {partition.device} ({partition.mountpoint})")
    
    while True:
        drive_choices = input("Enter the numbers of the drives to update (separated by commas): ")
        drive_numbers = [int(choice) for choice in drive_choices.split(',') if choice.isdigit()]
        if all(1 <= choice <= len(partitions) for choice in drive_numbers):
            break
        else:
            print("Invalid choice. Please enter valid numbers.")
    
    include_subfolders = input("Include subfolders? (yes/no): ").lower() == 'yes'
    
    conn = sqlite3.connect(db_path)
    create_files_table(conn)
    
    total_files = sum(len(os.listdir(partitions[choice - 1].mountpoint)) for choice in drive_numbers)
    progress_bar = tqdm(total=total_files, desc="Updating database", unit="file")
    start_time = datetime.now()
    processed_files = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(update_database_for_drive, partitions[choice - 1].mountpoint, excluded_file_types, excluded_directories) for choice in drive_numbers]
        for future in concurrent.futures.as_completed(futures):
            processed_files.extend(future.result())
            progress_bar.update(len(future.result()))
    progress_bar.close()
    insert_files(conn, processed_files)
    end_time = datetime.now()
    time_elapsed = (end_time - start_time).total_seconds()
    print(f"Database '{db_path}' updated successfully.")
    print(f"Time elapsed: {time_elapsed:.2f} seconds.")
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
