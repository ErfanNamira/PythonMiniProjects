import os
import sqlite3

def create_connection(db_file):
    """Create a connection to the SQLite database."""
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
        return None

def list_video_files(directory, include_subfolders=False):
    """List video files in the given directory."""
    video_files = []
    for root, dirs, files in os.walk(directory):
        if include_subfolders or root == directory:
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

def insert_video(conn, file_name, directory):
    """Insert a single video file into the database."""
    try:
        cursor = conn.cursor()
        file_path = os.path.join(directory, file_name)
        file_size_mb = round(os.path.getsize(file_path) / (1024 ** 2))
        cursor.execute("INSERT INTO video (file_name, directory, file_size_mb) VALUES (?, ?, ?)", (file_name, directory, file_size_mb))
        conn.commit()
    except sqlite3.Error as e:
        print(e)

def insert_videos(conn, videos):
    """Insert video files into the database."""
    try:
        cursor = conn.cursor()
        for video in videos:
            file_name, directory, file_size_mb = video
            cursor.execute("SELECT COUNT(*) FROM video WHERE file_name = ? AND directory = ?", (file_name, directory))
            count = cursor.fetchone()[0]
            if count == 0:
                cursor.execute("INSERT INTO video (file_name, directory, file_size_mb) VALUES (?, ?, ?)", (file_name, directory, file_size_mb))
        conn.commit()
        print("Movies added to the database successfully!")
    except sqlite3.Error as e:
        print(e)

def export_database(conn, output_file):
    """Export the database to a .txt file."""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM video")
        with open(output_file, 'w') as f:
            for row in cursor.fetchall():
                f.write(f"{row[0]} | {row[1]} | {row[3]} | {row[2]}\n")
        print(f"Database exported to {output_file} successfully!")
    except sqlite3.Error as e:
        print(e)

def check_similar_records(conn):
    """Check for similar records based on movie name."""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT file_name, COUNT(*) FROM video GROUP BY file_name HAVING COUNT(*) > 1")
        similar_records = cursor.fetchall()
        if similar_records:
            print("Similar records found:")
            for record in similar_records:
                print(record[0])  # Print movie name
        else:
            print("No similar records found.")
    except sqlite3.Error as e:
        print(e)

def main():
    print("Welcome to CineVault Video Database Management!")
    while True:
        print("\nMain Menu:")
        print("1. Scan directory for video files and create database")
        print("2. Add a single movie to the database")
        print("3. Update database with new movie files")
        print("4. Export database to a text file")
        print("5. Check for similar records based on movie name")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            directory = input("Enter the directory containing video files: ")
            include_subfolders = input("Include subfolders? (yes/no): ").lower() == "yes"
            save_as_new = input("Do you want to save the database with a new unique name? (yes/no): ").lower()
            db_file = f"video_database_{os.path.basename(os.path.normpath(directory))}.db" if save_as_new == "yes" else "video_database.db"
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
            directory = input("Enter the directory containing the movie file: ")
            file_name = input("Enter the name of the movie file: ")
            save_as_new = input("Do you want to save the database with a new unique name? (yes/no): ").lower()
            db_file = f"video_database_{os.path.basename(os.path.normpath(directory))}.db" if save_as_new == "yes" else "video_database.db"
            db_file_path = os.path.join(os.getcwd(), db_file)
            conn = create_connection(db_file_path)
            if conn is not None:
                create_video_table(conn)
                insert_video(conn, file_name, directory)
                conn.close()
                print("Movie added to the database successfully!")
                input("Press Enter to return to the main menu...")
            else:
                print("Error: Unable to create or connect to the database.")

        elif choice == "3":
            database_file = input("Enter the database address that should be updated: ")
            directory = input("Enter the directory containing new movie files: ")
            db_file_path = os.path.join(os.getcwd(), database_file)
            conn = create_connection(db_file_path)
            if conn is not None:
                create_video_table(conn)
                videos = list_video_files(directory, include_subfolders=True)
                insert_videos(conn, videos)
                conn.close()
                print("Database updated successfully!")
                input("Press Enter to return to the main menu...")
            else:
                print("Error: Unable to create or connect to the database.")

        elif choice == "4":
            database_file = input("Enter the database address that should be exported: ")
            output_file = input("Enter the name of the output .txt file: ")
            db_file_path = os.path.join(os.getcwd(), database_file)
            conn = create_connection(db_file_path)
            if conn is not None:
                export_database(conn, output_file)
                conn.close()
                input("Press Enter to return to the main menu...")
            else:
                print("Error: Unable to create or connect to the database.")

        elif choice == "5":
            db_file = input("Enter the path of the database file: ")
            db_file_path = os.path.join(os.getcwd(), db_file)
            conn = create_connection(db_file_path)
            if conn is not None:
                check_similar_records(conn)
                conn.close()
                input("Press Enter to return to the main menu...")
            else:
                print("Error: Unable to create or connect to the database.")

        elif choice == "6":
            print("Exiting the program...")
            break

        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()
