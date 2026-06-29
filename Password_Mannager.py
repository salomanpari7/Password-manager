from cryptography.fernet import Fernet
import os

KEY_FILE = "secret.key"
DATA_FILE = "passwords.enc"


# Create or load encryption key
def load_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
    else:
        with open(KEY_FILE, "rb") as f:
            key = f.read()
    return key


key = load_key()
cipher = Fernet(key)


# Add a password
def add_password():
    website = input("Website: ")
    username = input("Username: ")
    password = input("Password: ")

    data = f"{website}|{username}|{password}\n"
    encrypted = cipher.encrypt(data.encode())

    with open(DATA_FILE, "ab") as f:
        f.write(encrypted + b"\n")

    print("Password saved securely!")


# View all passwords
def view_passwords():
    if not os.path.exists(DATA_FILE):
        print("No passwords stored.")
        return

    print("\nStored Passwords")
    print("-" * 40)

    with open(DATA_FILE, "rb") as f:
        for line in f:
            decrypted = cipher.decrypt(line.strip()).decode()
            website, username, password = decrypted.split("|")

            print("Website :", website)
            print("Username:", username)
            print("Password:", password)
            print("-" * 40)


# Main menu
while True:
    print("\n==== ENCRYPTED PASSWORD MANAGER ====")
    print("1. Add Password")
    print("2. View Passwords")
    print("3. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        add_password()
    elif choice == "2":
        view_passwords()
    elif choice == "3":
        print("Exiting...")
        break
    else:
        print("Invalid choice.")
