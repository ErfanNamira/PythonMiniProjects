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

def main():
    print("Welcome to the Video Database Management System!")
    while True:
        print("\nMain Menu:")
        print("1. List video files in a database")
        print("2. Add a single movie to the database")
        print("3. Update a database with new movie files")
        print("4. Export database to a .txt file")
        print("5. Exit")

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
            directory = input("Enter the directory containing the movie file: ")
            file_name = input("Enter the name of the movie file: ")
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
                update_database(conn, db_file_path, directory)
                conn.close()
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
            print("Exiting the program...")
            break

        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()
