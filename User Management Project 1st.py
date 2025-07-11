import json
import os

# Step 1: Load users from file or create file
def load_users():
    if not os.path.exists("users.json"):
        with open("users.json", "w") as f:
            json.dump({}, f)
    with open("users.json", "r") as f:
        return json.load(f)

# Step 2: Save users to file
def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f)

# Step 3: Register a new user
def register_user():
    users = load_users()
    username = input("Enter a new username: ")
    if username in users:
        print("Username already exists. Try another one.")
        return
    password = input("Enter a password: ")
    users[username] = password
    save_users(users)
    print("✅ Registered successfully!")

# Step 4: Login existing user
def login_user():
    users = load_users()
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    if users.get(username) == password:
        print(f"✅ Login successful! Welcome, {username}")
        after_login_menu(username)
    else:
        print("❌ Incorrect username or password.")

# Step 5: After login menu - update or delete account
def after_login_menu(username):
    while True:
        print("\n1. Update Password")
        print("2. Delete Account")
        print("3. Logout")
        choice = input("Enter your choice: ")

        users = load_users()

        if choice == "1":
            new_password = input("Enter new password: ")
            users[username] = new_password
            save_users(users)
            print("🔐 Password updated!")

        elif choice == "2":
            confirm = input("Are you sure you want to delete your account? (yes/no): ")
            if confirm.lower() == "yes":
                users.pop(username)
                save_users(users)
                print("🗑️ Account deleted.")
                break

        elif choice == "3":
            print("🚪 Logged out.")
            break

        else:
            print("⚠️ Invalid choice. Try again.")

# Step 6: Main menu for all users
def main_menu():
    while True:
        print("\n===== USER MANAGEMENT SYSTEM =====")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            register_user()
        elif choice == "2":
            login_user()
        elif choice == "3":
            print("👋 Thank you! Exiting system.")
            break
        else:
            print("⚠️ Invalid choice. Please try again.")

# Step 7: Start the program
if __name__ == "__main__":
    main_menu()
