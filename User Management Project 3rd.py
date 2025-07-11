# FINAL WORKING USER MANAGEMENT SYSTEM
# Modern GUI, SQLite, Login via Username or Email, OTP Password Reset

import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3
import hashlib
import smtplib
import ssl
import random

# -------------------- CONFIG --------------------
DB_NAME = 'users.db'
SENDER_EMAIL = 'your_email@gmail.com'       # <-- Replace with your email
APP_PASSWORD = 'your_app_password'          # <-- Use Gmail App Password

# -------------------- UTILITY FUNCTIONS --------------------
def encrypt_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def send_otp(email, otp):
    message = f"Subject: OTP Verification\n\nYour OTP is: {otp}"
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.sendmail(SENDER_EMAIL, email, message)
        return True
    except Exception as e:
        messagebox.showerror("Email Error", f"Failed to send OTP.\n{e}")
        return False

# -------------------- DB SETUP --------------------
conn = sqlite3.connect(DB_NAME)
conn.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT UNIQUE,
    email TEXT UNIQUE,
    password TEXT
);
""")
conn.close()

# -------------------- CORE FUNCTIONS --------------------
def register_user(username, email, password):
    if not (username and email and password):
        messagebox.showerror("Error", "All fields required")
        return

    encrypted = encrypt_password(password)
    try:
        with sqlite3.connect(DB_NAME) as conn:
            conn.execute("INSERT INTO users VALUES (?, ?, ?)", (username, email, encrypted))
        messagebox.showinfo("Success", "Registered successfully!")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username or Email already exists")

def login_user(identifier, password):
    encrypted = encrypt_password(password)
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute("SELECT username FROM users WHERE (email=? COLLATE NOCASE OR username=? COLLATE NOCASE) AND password=?",
                    (identifier, identifier, encrypted))
        result = cur.fetchone()
        if result:
            messagebox.showinfo("Login", f"Welcome {result[0]}!")
        else:
            messagebox.showerror("Login Failed", "Invalid credentials")

def reset_password(email):
    if not email:
        messagebox.showerror("Error", "Enter your registered email")
        return
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email=?", (email,))
        if not cur.fetchone():
            messagebox.showerror("Error", "Email not found")
            return

    otp = str(random.randint(1000, 9999))
    if not send_otp(email, otp):
        return
    user_otp = simpledialog.askstring("OTP", "Enter the OTP sent to your email")
    if user_otp != otp:
        messagebox.showerror("Error", "Incorrect OTP")
        return

    new_pass = simpledialog.askstring("New Password", "Enter new password", show='*')
    if not new_pass:
        messagebox.showerror("Error", "Password can't be empty")
        return

    enc = encrypt_password(new_pass)
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("UPDATE users SET password=? WHERE email=?", (enc, email))
    messagebox.showinfo("Success", "Password updated!")

def delete_account(identifier):
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM users WHERE email=? OR username=?", (identifier, identifier))
        if cur.rowcount:
            messagebox.showinfo("Deleted", "Account deleted successfully")
        else:
            messagebox.showerror("Error", "No account found")

# -------------------- GUI SETUP --------------------
def launch_gui():
    root = tk.Tk()
    root.title("User Login")
    root.geometry("400x550")
    root.config(bg="#eaf6ff")

    def clear():
        for widget in root.winfo_children():
            widget.destroy()

    def styled_entry(parent):
        entry = tk.Entry(parent, width=30, font=("Arial", 12), bd=2, relief="solid")
        entry.pack(pady=5)
        return entry

    def styled_button(parent, text, cmd):
        return tk.Button(parent, text=text, command=cmd, bg="#007acc", fg="white", font=("Arial", 10), width=20, relief="flat")

    def login_screen():
        clear()
        tk.Label(root, text="📱 InstaStyle Login", font=("Helvetica", 20, "bold"), bg="#eaf6ff", fg="#333").pack(pady=30)

        tk.Label(root, text="Email or Username", bg="#eaf6ff").pack()
        entry_id = styled_entry(root)

        tk.Label(root, text="Password", bg="#eaf6ff").pack()
        entry_pass = styled_entry(root)
        entry_pass.config(show="*")

        styled_button(root, "Login", lambda: login_user(entry_id.get(), entry_pass.get())).pack(pady=10)
        tk.Button(root, text="Forgot Password?", bg="#eaf6ff", command=lambda: reset_password(entry_id.get()), fg="blue", relief="flat").pack()
        tk.Button(root, text="Delete Account", bg="#eaf6ff", command=lambda: delete_account(entry_id.get()), fg="red", relief="flat").pack(pady=5)

        tk.Label(root, text="New here?", bg="#eaf6ff").pack(pady=15)
        styled_button(root, "Create New Account", register_screen).pack()

    def register_screen():
        clear()
        tk.Label(root, text="📲 Create Account", font=("Helvetica", 20, "bold"), bg="#eaf6ff", fg="#333").pack(pady=30)

        tk.Label(root, text="Username", bg="#eaf6ff").pack()
        new_user = styled_entry(root)

        tk.Label(root, text="Email", bg="#eaf6ff").pack()
        new_email = styled_entry(root)

        tk.Label(root, text="Password", bg="#eaf6ff").pack()
        new_pass = styled_entry(root)
        new_pass.config(show="*")

        styled_button(root, "Register", lambda: register_user(new_user.get(), new_email.get(), new_pass.get())).pack(pady=10)
        tk.Button(root, text="Back to Login", bg="#eaf6ff", fg="blue", command=login_screen, relief="flat").pack()

    login_screen()
    root.mainloop()

if __name__ == '__main__':
    launch_gui()
