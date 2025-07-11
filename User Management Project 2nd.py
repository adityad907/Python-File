import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3, hashlib, random, smtplib, ssl

# ---- Database Setup ----
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                        username TEXT PRIMARY KEY,
                        password TEXT NOT NULL,
                        email TEXT NOT NULL)""")
    conn.commit(); conn.close()
init_db()

# ---- Password Encryption ----
def encrypt_password(pw): return hashlib.sha256(pw.encode()).hexdigest()

# ---- Send OTP by Email ----
def send_otp(email, otp):
    try:
        port = 465
        smtp_server = "smtp.gmail.com"
        sender = "<YOUR_EMAIL@gmail.com>"
        password = "<YOUR_APP_PASSWORD>"
        receiver = email
        message = f"Subject: Your OTP Code\n\nYour OTP is: {otp}"
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender, password)
            server.sendmail(sender, receiver, message)
        return True
    except Exception as e:
        print("Email error:", e)
        return False

# ---- GUI Back-End Functions ----

def register():
    u = ent_user.get().strip()
    pw = ent_pass.get().strip()
    em = ent_email.get().strip()
    if not (u and pw and em):
        return messagebox.showerror("Error", "Fill all fields")
    pw_hash = encrypt_password(pw)
    try:
        conn = sqlite3.connect("users.db")
        conn.execute("INSERT INTO users VALUES (?, ?, ?)", (u, pw_hash, em))
        conn.commit(); conn.close()
        messagebox.showinfo("Success", "Registration complete!")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists!")

def login():
    u = ent_user.get().strip()
    pw_hash = encrypt_password(ent_pass.get().strip())
    conn = sqlite3.connect("users.db")
    cur = conn.execute("SELECT * FROM users WHERE username=? AND password=?", (u, pw_hash))
    if cur.fetchone():
        messagebox.showinfo("Welcome", f"Hi {u}!")
        dashboard(u)
    else:
        messagebox.showerror("Error", "Bad credentials.")
    conn.close()

def dashboard(username):
    win = tk.Toplevel(root)
    win.title("Dashboard")
    tk.Label(win, text=f"Welcome, {username}", font=("",14)).pack(pady=5)

    tk.Label(win, text="New Password:").pack()
    npw = tk.Entry(win, show="*"); npw.pack()
    tk.Button(win, text="Update Password", command=lambda: update_pwd(username,npw.get(),win)).pack(pady=3)
    tk.Button(win, text="Delete Account", command=lambda: del_account(username,win)).pack(pady=3)
    tk.Button(win, text="Logout", command=win.destroy).pack(pady=5)

def update_pwd(username, newpw, window):
    if not newpw:
        return messagebox.showerror("Error", "Enter new password")
    conn = sqlite3.connect("users.db")
    conn.execute("UPDATE users SET password=? WHERE username=?", (encrypt_password(newpw), username))
    conn.commit(); conn.close()
    messagebox.showinfo("Done", "Password updated!")

def del_account(username, window):
    if not messagebox.askyesno("Confirm", "Delete your account?"): return
    conn = sqlite3.connect("users.db")
    conn.execute("DELETE FROM users WHERE username=?", (username,))
    conn.commit(); conn.close()
    messagebox.showinfo("Deleted", "Account deleted")
    window.destroy()

def forgot_pwd():
    u = simpledialog.askstring("Username", "Enter your username:")
    if not u:
        return
    conn = sqlite3.connect("users.db")
    cur = conn.execute("SELECT email FROM users WHERE username=?", (u,))
    row = cur.fetchone(); conn.close()
    if not row:
        return messagebox.showerror("Error", "User not found")
    em = row[0]; otp = str(random.randint(100000,999999))
    if not send_otp(em, otp):
        return messagebox.showerror("Error", "Failed to send OTP")
    usr_otp = simpledialog.askstring("OTP", "Enter the OTP sent to your email:")
    if usr_otp != otp:
        return messagebox.showerror("Error", "Wrong OTP")
    newpw = simpledialog.askstring("New Password", "Enter your new password:", show="*")
    if not newpw:
        return messagebox.showerror("Error", "Password cannot be empty")
    conn = sqlite3.connect("users.db")
    conn.execute("UPDATE users SET password=? WHERE username=?", (encrypt_password(newpw), u))
    conn.commit(); conn.close()
    messagebox.showinfo("Success", "Password reset!")

# ---- GUI Setup ----
root = tk.Tk(); root.title("User Management System")
tk.Label(root, text="Username:").grid(row=0, column=0, pady=2)
ent_user = tk.Entry(root); ent_user.grid(row=0, column=1, pady=2)
tk.Label(root, text="Password:").grid(row=1, column=0, pady=2)
ent_pass = tk.Entry(root, show="*"); ent_pass.grid(row=1, column=1, pady=2)
tk.Label(root, text="Email (for OTP):").grid(row=2, column=0, pady=2)
ent_email = tk.Entry(root); ent_email.grid(row=2, column=1, pady=2)

tk.Button(root, text="Register", width=12, command=register).grid(row=3, column=0, pady=5)
tk.Button(root, text="Login", width=12, command=login).grid(row=3, column=1)
tk.Button(root, text="Forgot Password", width=26, command=forgot_pwd).grid(row=4, column=0, columnspan=2, pady=3)

root.mainloop()
