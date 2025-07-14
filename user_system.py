
"""
user_system.py
==============
A full-featured User Management System (console-based) that includes:

1. Persistent JSON storage
2. User Registration with:
   - Email format validation
   - Password strength check
   - Unique email enforcement
   - Initial status = 'inactive'
3. Email verification simulation
4. Login with status check
5. Password update with current password check
6. Account deletion with confirmation
7. Admin role view (admin can list all users)
8. Console menu interface
9. Error handling for corrupted/missing DB
10. User-friendly messages

Run this script with:  python user_system.py
"""

import json
import os
import re

DB_FILE = "user_data.json"

def load_db():
    if not os.path.exists(DB_FILE):
        return {}
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("⚠️ Database file is corrupted. Starting with empty DB.")
        return {}

def save_db(db):
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=4)

def is_valid_email(email):
    return re.fullmatch(r"^[^@]+@[^@]+\.[^@]+$", email)

def is_strong_password(password):
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$'
    return re.fullmatch(pattern, password)

def register():
    db = load_db()
    email = input("Enter your email: ").strip()
    if not is_valid_email(email):
        print("❌ Invalid email format.")
        return
    if email in db:
        print("❌ This email is already registered.")
        return
    password = input("Create a strong password: ").strip()
    if not is_strong_password(password):
        print("❌ Password too weak (must include U/L/digit/symbol and be 8+ chars).")
        return
    db[email] = {"password": password, "status": "inactive"}
    save_db(db)
    print("✅ Registered successfully! Please verify your email to activate your account.")

def verify_email():
    db = load_db()
    email = input("Enter your email to verify: ").strip()
    if email in db:
        db[email]["status"] = "active"
        save_db(db)
        print("✅ Email verified. Your account is now active.")
    else:
        print("❌ Email not found.")

def login():
    db = load_db()
    email = input("Enter your email: ").strip()
    password = input("Enter your password: ").strip()
    if email not in db:
        print("❌ Email not registered.")
        return
    if db[email]["status"] != "active":
        print("⚠️ Account is not active. Please verify your email.")
        return
    if db[email]["password"] != password:
        print("❌ Incorrect password.")
        return
    print(f"🎉 Logged in successfully as {email}")
    if email == "admin@gmail.com":
        admin_view()

def admin_view():
    db = load_db()
    print("\n🔐 Admin View - All Registered Users:")
    for user, info in db.items():
        print(f" - {user} (Status: {info['status']})")

def update_password():
    db = load_db()
    email = input("Enter your email: ").strip()
    current = input("Enter current password: ").strip()
    if email not in db:
        print("❌ Email not found.")
        return
    if db[email]["password"] != current:
        print("❌ Incorrect current password.")
        return
    new = input("Enter new password: ").strip()
    confirm = input("Confirm new password: ").strip()
    if new != confirm:
        print("❌ Passwords do not match.")
        return
    if not is_strong_password(new):
        print("❌ New password too weak.")
        return
    db[email]["password"] = new
    save_db(db)
    print("✅ Password updated successfully.")

def delete_account():
    db = load_db()
    email = input("Enter your email: ").strip()
    current = input("Enter your password: ").strip()
    if email not in db:
        print("❌ Email not found.")
        return
    if db[email]["password"] != current:
        print("❌ Incorrect password.")
        return
    confirm = input("Are you sure you want to delete your account? (yes/no): ").strip().lower()
    if confirm == "yes":
        del db[email]
        save_db(db)
        print("✅ Account deleted successfully.")
    else:
        print("❎ Account deletion cancelled.")

def main_menu():
    while True:
        print("\n===== USER MANAGEMENT MENU =====")
        print("1) Register")
        print("2) Verify Email")
        print("3) Login")
        print("4) Update Password")
        print("5) Delete Account")
        print("6) Exit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            register()
        elif choice == "2":
            verify_email()
        elif choice == "3":
            login()
        elif choice == "4":
            update_password()
        elif choice == "5":
            delete_account()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please select from the menu.")

if __name__ == "__main__":
    main_menu()
