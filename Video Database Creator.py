import os
import sqlite3

def create_connection(db_file):
    """Create a database connection to the SQLite database."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

def list_video_files(directory, include_subfolders=False):
    """List video files in the given directory."""
    video_files = []
    for root, dirs, files in os.walk(directory):
        if include_subfolders or root == directory:  # Include subfolders only if specified or if it's the main directory
            for file in files:
                if file.endswith((".mkv", ".mp4")):
                    file_path = os.path.join(root, file)
                    video_files.append((file, file_path, round(os.path.getsize(file_path) / (1024 ** 2))))
    return video_files

def create_video_table(conn):
    """Create a video table in the database."""
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS video (
                id INTEGER PRIMARY KEY,
                file_name TEXT,
                directory TEXT,
                file_size_mb INTEGER
            )
        """)
        conn.commit()
    except sqlite3.Error as e:
        print(e)

def insert_videos(conn, videos):
    """Insert video files into the database."""
    try:
        cursor = conn.cursor()
        cursor.executemany("INSERT INTO video (file_name, directory, file_size_mb) VALUES (?, ?, ?)", videos)
        conn.commit()
    except sqlite3.Error as e:
        print(e)

def main():
    print("Welcome to the Video Database Management System!")
    while True:
        print("\nMain Menu:")
        print("1. List video files in a database")
        print("2. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            directory = input("Enter the directory containing video files: ")
            include_subfolders = input("Include subfolders? (yes/no): ").lower() == "yes"
            save_as_new = input("Do you want to save the database with a new unique name? (yes/no): ").lower()
            if save_as_new == "yes":
                folder_name = os.path.basename(os.path.normpath(directory))
                db_file = f"video_database_{folder_name}.db"
            else:
                db_file = "video_database.db"
            db_file_path = os.path.join(os.getcwd(), db_file)
            conn = create_connection(db_file_path)
            if conn is not None:
                create_video_table(conn)
                videos = list_video_files(directory, include_subfolders)
                insert_videos(conn, videos)
                conn.close()
                print("Video files listed successfully!")
                input("Press Enter to return to the main menu...")
            else:
                print("Error: Unable to create or connect to the database.")

        elif choice == "2":
            print("Exiting the program...")
            break

        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()
