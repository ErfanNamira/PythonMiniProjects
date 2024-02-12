import os
import sqlite3
import shutil
from datetime import datetime

# Function to create a database from a directory
def create_database():
    directory = input("Enter the directory path: ")
    format_option = input("Enter the file format to query (e.g., .jpg) or enter 'all' for all formats: ")
    include_subfolders = input("Include subfolders? (yes/no): ").lower() == 'yes'
    db_name = input("Enter the database name (without extension): ")
    if not db_name.endswith('.db'):
        db_name += '.db'
    conn = sqlite3.connect(db_name)
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
    for root, dirs, files in os.walk(directory):
        for name in files:
            file_path = os.path.join(root, name)
            file_format = os.path.splitext(name)[-1].lower()
            if format_option == 'all' or file_format == format_option:
                c.execute("SELECT * FROM files WHERE address=?", (file_path,))
                if not c.fetchone():
                    size = int(os.path.getsize(file_path) / 1024)
                    created_date = datetime.fromtimestamp(os.path.getctime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
                    c.execute("INSERT INTO files (type, file_format, name, address, size, created_date) VALUES (?, ?, ?, ?, ?, ?)",
                              ('file', file_format, name, file_path, size, created_date))
    if include_subfolders:
        for root, dirs, files in os.walk(directory):
            for name in dirs:
                dir_path = os.path.join(root, name)
                c.execute("SELECT * FROM files WHERE address=?", (dir_path,))
                if not c.fetchone():
                    created_date = datetime.fromtimestamp(os.path.getctime(dir_path)).strftime('%Y-%m-%d %H:%M:%S')
                    c.execute("INSERT INTO files (type, name, address, created_date) VALUES (?, ?, ?, ?)",
                              ('folder', name, dir_path, created_date))
    conn.commit()
    conn.close()
    print(f"Database '{db_name}' created successfully.")

# Function to add a single file to the database
def add_single_file():
    directory = input("Enter the directory path: ")
    file_name = input("Enter the file name: ")
    db_path = input("Enter the path to the database: ")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    file_path = os.path.join(directory, file_name)
    if not os.path.exists(file_path):
        print("File does not exist.")
        conn.close()
        return
    file_format = os.path.splitext(file_name)[-1].lower()
    c.execute("SELECT * FROM files WHERE address=?", (file_path,))
    if not c.fetchone():
        size = int(os.path.getsize(file_path) / 1024)
        created_date = datetime.fromtimestamp(os.path.getctime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
        c.execute("INSERT INTO files (type, file_format, name, address, size, created_date) VALUES (?, ?, ?, ?, ?, ?)",
                  ('file', file_format, file_name, file_path, size, created_date))
        print("File added successfully.")
    else:
        print("File already exists in the database.")
    conn.commit()
    conn.close()

# Function to update a database
def update_database():
    db_path = input("Enter the path to the database: ")  # Prompt for database path
    directory = input("Enter the directory path: ")
    include_subfolders = input("Include subfolders? (yes/no): ").lower() == 'yes'
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    for root, dirs, files in os.walk(directory):
        for name in files:
            file_path = os.path.join(root, name)
            c.execute("SELECT * FROM files WHERE address=?", (file_path,))
            if not c.fetchone():
                file_format = os.path.splitext(name)[-1].lower()
                size = int(os.path.getsize(file_path) / 1024)
                created_date = datetime.fromtimestamp(os.path.getctime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
                c.execute("INSERT INTO files (type, file_format, name, address, size, created_date) VALUES (?, ?, ?, ?, ?, ?)",
                          ('file', file_format, name, file_path, size, created_date))
    if include_subfolders:
        for root, dirs, files in os.walk(directory):
            for name in dirs:
                dir_path = os.path.join(root, name)
                c.execute("SELECT * FROM files WHERE address=?", (dir_path,))
                if not c.fetchone():
                    created_date = datetime.fromtimestamp(os.path.getctime(dir_path)).strftime('%Y-%m-%d %H:%M:%S')
                    c.execute("INSERT INTO files (type, name, address, created_date) VALUES (?, ?, ?, ?)",
                              ('folder', name, dir_path, created_date))
    conn.commit()
    conn.close()
    print("Database updated successfully.")

# Function to export a database to a .txt file
def export_database():
    db_path = input("Enter the path to the database: ") 
    txt_file = input("Enter the .txt file name to export: ")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT * FROM files")
    with open(txt_file, 'w', encoding='utf-8') as f:  
        for row in c.fetchall():
            f.write(','.join(map(str, row)) + '\n')
    conn.close()
    print(f"Database '{db_path}' exported to '{txt_file}' successfully.")

# Main function
def main():
    while True:
        print("\nMENU:")
        print("1. Create Database from a directory")
        print("2. Add a single file to the database")
        print("3. Update a database")
        print("4. Export a database to a .txt file")
        print("5. Exit")
        choice = input("Enter your choice (1-5): ")
        if choice == '1':
            create_database()
        elif choice == '2':
            add_single_file()
        elif choice == '3':
            update_database()
        elif choice == '4':
            export_database()
        elif choice == '5':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 5.")

if __name__ == "__main__":
    main()