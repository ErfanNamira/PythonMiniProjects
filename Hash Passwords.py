# Hash Passwords
# Python Mini Projects
# ErfanNamira
# https://github.com/ErfanNamira/PythonMiniProjects

from passlib.hash import sha256_crypt

def main():
    password = input("Enter the password you want to hash: ")

    # Hash the entered password
    hashed_password = sha256_crypt.hash(password)

    print("Hashed Password:", hashed_password)

if __name__ == "__main__":
    main()