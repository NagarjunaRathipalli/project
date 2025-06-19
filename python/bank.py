import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3
from datetime import datetime

conn = sqlite3.connect("bank.db")
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    pin TEXT,
    balance REAL DEFAULT 0.0
)''')

c.execute('''CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    date TEXT,
    amount REAL,
    type TEXT,
    FOREIGN KEY(user_id) REFERENCES users(user_id)
)''')

c.execute('''CREATE TABLE IF NOT EXISTS admins (
    admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
)''')

c.execute("SELECT * FROM admins WHERE username='admin'")
if not c.fetchone():
    c.execute("INSERT INTO admins (username, password) VALUES (?, ?)", ("admin", "admin123"))

conn.commit()

def draw_gradient(canvas, color1, color2):
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    canvas.delete("gradient")

    r1, g1, b1 = canvas.winfo_rgb(color1)
    r2, g2, b2 = canvas.winfo_rgb(color2)

    r_ratio = (r2 - r1) / width
    g_ratio = (g2 - g1) / width
    b_ratio = (b2 - b1) / width

    for i in range(width):
        nr = int(r1 + (r_ratio * i))
        ng = int(g1 + (g_ratio * i))
        nb = int(b1 + (b_ratio * i))
        color = f'#{nr//256:02x}{ng//256:02x}{nb//256:02x}'
        canvas.create_line(i, 0, i, height, tags=("gradient",), fill=color)

class BankingApp:
    def _init_(self, root):
        self.root = root
        self.root.title("Banking Application")
        self.root.geometry("500x400")
        self.current_user_id = None
        self.canvas = tk.Canvas(self.root, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", lambda e: draw_gradient(self.canvas, "#2c3e50", "#4ca1af"))

        self.frame = tk.Frame(self.canvas, bg="#2c3e50")
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

        self.main_menu()

    def clear_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

    def main_menu(self):
        self.clear_frame()
        tk.Label(self.frame, text="Banking System", font=("Arial", 20), fg="white", bg="#2c3e50").pack(pady=20)
        tk.Button(self.frame, text="User Login", command=self.user_login, bg="white", fg="#2c3e50", width=20).pack(pady=5)
        tk.Button(self.frame, text="Register", command=self.register_user, bg="white", fg="#2c3e50", width=20).pack(pady=5)
        tk.Button(self.frame, text="Admin Login", command=self.admin_login, bg="white", fg="#2c3e50", width=20).pack(pady=5)

    def register_user(self):
        self.clear_frame()
        tk.Label(self.frame, text="Register", font=("Arial", 18), fg="white", bg="#2c3e50").pack(pady=10)

        name_entry = tk.Entry(self.frame)
        pin_entry = tk.Entry(self.frame, show="*")

        tk.Label(self.frame, text="Name", fg="white", bg="#2c3e50").pack()
        name_entry.pack()
        tk.Label(self.frame, text="PIN (4 digits)", fg="white", bg="#2c3e50").pack()
        pin_entry.pack()

        def register():
            name = name_entry.get()
            pin = pin_entry.get()
            if name and pin.isdigit() and len(pin) == 4:
                c.execute("INSERT INTO users (name, pin) VALUES (?, ?)", (name, pin))
                conn.commit()
                user_id = c.lastrowid
                messagebox.showinfo("Success", f"Account created!\nYour User ID is: {user_id}")
                self.main_menu()
            else:
                messagebox.showerror("Error", "Invalid name or PIN")

        tk.Button(self.frame, text="Register", command=register, bg="white", fg="#2c3e50").pack(pady=10)
        tk.Button(self.frame, text="Back", command=self.main_menu, bg="white", fg="#2c3e50").pack()

    def user_login(self):
        self.clear_frame()
        tk.Label(self.frame, text="User Login", font=("Arial", 18), fg="white", bg="#2c3e50").pack(pady=10)

        id_entry = tk.Entry(self.frame)
        pin_entry = tk.Entry(self.frame, show="*")

        tk.Label(self.frame, text="User ID", fg="white", bg="#2c3e50").pack()
        id_entry.pack()
        tk.Label(self.frame, text="PIN", fg="white", bg="#2c3e50").pack()
        pin_entry.pack()

        def login():
            uid = id_entry.get()
            pin = pin_entry.get()
            c.execute("SELECT * FROM users WHERE user_id=? AND pin=?", (uid, pin))
            user = c.fetchone()
            if user:
                self.current_user_id = user[0]
                self.user_dashboard()
            else:
                messagebox.showerror("Error", "Invalid credentials")

        tk.Button(self.frame, text="Login", command=login, bg="white", fg="#2c3e50").pack(pady=10)
        tk.Button(self.frame, text="Back", command=self.main_menu, bg="white", fg="#2c3e50").pack()

    def user_dashboard(self):
        self.clear_frame()
        tk.Label(self.frame, text="User Dashboard", font=("Arial", 18), fg="white", bg="#2c3e50").pack(pady=10)
        tk.Button(self.frame, text="View Balance", command=self.view_balance, bg="white", fg="#2c3e50", width=20).pack(pady=5)
        tk.Button(self.frame, text="Deposit Money", command=self.deposit_money, bg="white", fg="#2c3e50", width=20).pack(pady=5)
        tk.Button(self.frame, text="Withdraw Money", command=self.withdraw_money, bg="white", fg="#2c3e50", width=20).pack(pady=5)
        tk.Button(self.frame, text="Logout", command=self.main_menu, bg="white", fg="#2c3e50", width=20).pack(pady=10)

    def view_balance(self):
        c.execute("SELECT balance FROM users WHERE user_id=?", (self.current_user_id,))
        balance = c.fetchone()[0]
        messagebox.showinfo("Balance", f"Your balance is ₹{balance:.2f}")

    def deposit_money(self):
        amount = simpledialog.askfloat("Deposit", "Enter amount to deposit:")
        if amount is None:
            return
        if amount <= 0:
            messagebox.showerror("Error", "Enter a positive amount")
            return
        c.execute("UPDATE users SET balance = balance + ? WHERE user_id=?", (amount, self.current_user_id))
        c.execute("INSERT INTO transactions (user_id, date, amount, type) VALUES (?, ?, ?, ?)",
                  (self.current_user_id, datetime.now(), amount, "deposit"))
        conn.commit()
        messagebox.showinfo("Success", "Deposit successful")

    def withdraw_money(self):
        amount = simpledialog.askfloat("Withdraw", "Enter amount to withdraw:")
        if amount is None:
            return
        if amount <= 0:
            messagebox.showerror("Error", "Enter a positive amount")
            return
        c.execute("SELECT balance FROM users WHERE user_id=?", (self.current_user_id,))
        balance = c.fetchone()[0]
        if amount > balance:
            messagebox.showerror("Error", "Insufficient balance")
            return
        c.execute("UPDATE users SET balance = balance - ? WHERE user_id=?", (amount, self.current_user_id))
        c.execute("INSERT INTO transactions (user_id, date, amount, type) VALUES (?, ?, ?, ?)",
                  (self.current_user_id, datetime.now(), amount, "withdrawal"))
        conn.commit()
        messagebox.showinfo("Success", "Withdrawal successful")

    def admin_login(self):
        self.clear_frame()
        tk.Label(self.frame, text="Admin Login", font=("Arial", 18), fg="white", bg="#2c3e50").pack(pady=10)

        username = tk.Entry(self.frame)
        password = tk.Entry(self.frame, show="*")

        tk.Label(self.frame, text="Username", fg="white", bg="#2c3e50").pack()
        username.pack()
        tk.Label(self.frame, text="Password", fg="white", bg="#2c3e50").pack()
        password.pack()

        def login():
            c.execute("SELECT * FROM admins WHERE username=? AND password=?", (username.get(), password.get()))
            if c.fetchone():
                self.admin_dashboard()
            else:
                messagebox.showerror("Error", "Invalid credentials")

        tk.Button(self.frame, text="Login", command=login, bg="white", fg="#2c3e50").pack(pady=10)
        tk.Button(self.frame, text="Back", command=self.main_menu, bg="white", fg="#2c3e50").pack()

    def admin_dashboard(self):
        self.clear_frame()
        tk.Label(self.frame, text="Admin Dashboard", font=("Arial", 18), fg="white", bg="#2c3e50").pack(pady=10)
        tk.Button(self.frame, text="View All Users", command=self.view_users, bg="white", fg="#2c3e50", width=20).pack(pady=5)
        tk.Button(self.frame, text="View All Transactions", command=self.view_transactions, bg="white", fg="#2c3e50", width=20).pack(pady=5)
        tk.Button(self.frame, text="Add User", command=self.add_user, bg="white", fg="#2c3e50", width=20).pack(pady=5)
        tk.Button(self.frame, text="Remove User", command=self.remove_user, bg="white", fg="#2c3e50", width=20).pack(pady=5)
        #tk.Button(self.frame, text="Back", command=self.main_menu, bg="white", fg="#2c3e50", width=20).pack(pady=10)
        tk.Button(self.frame, text="Logout", command=self.main_menu, bg="white", fg="#2c3e50", width=20).pack(pady=10)

    def view_users(self):
        c.execute("SELECT user_id, name, balance FROM users")
        data = c.fetchall()
        info = "\n".join([f"ID: {d[0]}, Name: {d[1]}, ₹{d[2]:.2f}" for d in data])
        messagebox.showinfo("Users", info or "No users found.")

    def view_transactions(self):
        c.execute("SELECT user_id, date, amount, type FROM transactions")
        data = c.fetchall()
        info = "\n".join([f"User {d[0]}: {d[3].capitalize()} ₹{d[2]:.2f} on {d[1]}" for d in data])
        messagebox.showinfo("Transactions", info or "No transactions found.")


    def add_user(self):
        name = simpledialog.askstring("Add User", "Enter user name:")
        pin = simpledialog.askstring("Add User", "Enter 4-digit PIN:")
        if name and pin and pin.isdigit() and len(pin) == 4:
            c.execute("INSERT INTO users (name, pin) VALUES (?, ?)", (name, pin))
            conn.commit()
            uid = c.lastrowid
            messagebox.showinfo("Success", f"User added with ID: {uid}")
        else:
            messagebox.showerror("Error", "Invalid input")

    def remove_user(self):
        uid = simpledialog.askinteger("Remove User", "Enter User ID to remove:")
        if uid is not None:
            c.execute("DELETE FROM users WHERE user_id=?", (uid,))
            conn.commit()
            messagebox.showinfo("Success", f"User {uid} removed.")

if _name_ == "_main_":
    root = tk.Tk()
    app = BankingApp(root)
    root.mainloop()