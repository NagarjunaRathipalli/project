import tkinter as tk
from tkinter import messagebox, simpledialog
import mysql.connector
from datetime import datetime

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="student",  
    database="bankdb"
)
c = conn.cursor()

class BankingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Banking System")
        self.root.geometry("500x400")
        self.current_user_id = None
        self.colors = {
            "main": "#2c3e50",
            "register": "#4ca1af",
            "user_login": "#2fb86e",
            "user_dashboard": "#854cb1",
            "admin_login": "#5bbfe9",
            "admin_dashboard": "#f4ab52"
        }
        self.main_menu()

    def clear_frame(self, color):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.configure(bg=color)

    def main_menu(self):
        self.clear_frame(self.colors["main"])
        tk.Label(self.root, text="Banking System", font=("Arial", 20), bg=self.colors["main"], fg="white").pack(pady=20)
        tk.Button(self.root, text="User Login", command=self.user_login, width=20).pack(pady=5)
        tk.Button(self.root, text="Register", command=self.register_user, width=20).pack(pady=5)
        tk.Button(self.root, text="Admin Login", command=self.admin_login, width=20).pack(pady=5)

    def register_user(self, return_to_admin=False):
        self.clear_frame(self.colors["register"])
        tk.Label(self.root, text="Register", font=("Arial", 18), bg=self.colors["register"], fg="white").pack(pady=10)

        name_entry = tk.Entry(self.root)
        email_entry = tk.Entry(self.root)
        phone_entry = tk.Entry(self.root)
        pass_entry = tk.Entry(self.root, show="*")

        for label, entry in [("Name", name_entry), ("Email", email_entry), ("Phone", phone_entry), ("Password", pass_entry)]:
            tk.Label(self.root, text=label, bg=self.colors["register"], fg="white").pack()
            entry.pack()

        def register():
            name = name_entry.get()
            email = email_entry.get()
            phone = phone_entry.get()
            password = pass_entry.get()
            if name and email and phone and password:
                c.execute("INSERT INTO Users (name, email, phone, password) VALUES (%s, %s, %s, %s)",
                          (name, email, phone, password))
                conn.commit()
                user_id = c.lastrowid
                c.execute("INSERT INTO Accounts (user_id, account_type, balance) VALUES (%s, %s, %s)",
                          (user_id, "Savings", 0.0))
                conn.commit()
                messagebox.showinfo("Success", f"Account created. User ID: {user_id}")
                self.admin_dashboard() if return_to_admin else self.main_menu()
            else:
                messagebox.showerror("Error", "Please fill all fields.")

        tk.Button(self.root, text="Submit", command=register).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.admin_dashboard if return_to_admin else self.main_menu).pack()

    def user_login(self):
        self.clear_frame(self.colors["user_login"])
        tk.Label(self.root, text="User Login", font=("Arial", 18), bg=self.colors["user_login"], fg="white").pack(pady=10)

        uid_entry = tk.Entry(self.root)
        pass_entry = tk.Entry(self.root, show="*")

        tk.Label(self.root, text="User ID", bg=self.colors["user_login"], fg="white").pack()
        uid_entry.pack()
        tk.Label(self.root, text="Password", bg=self.colors["user_login"], fg="white").pack()
        pass_entry.pack()

        def login():
            uid = uid_entry.get()
            pwd = pass_entry.get()
            c.execute("SELECT * FROM Users WHERE user_id=%s AND password=%s", (uid, pwd))
            user = c.fetchone()
            if user:
                self.current_user_id = int(uid)
                self.user_dashboard()
            else:
                messagebox.showerror("Error", "Invalid credentials")

        tk.Button(self.root, text="Login", command=login).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.main_menu).pack()

    def user_dashboard(self):
        self.clear_frame(self.colors["user_dashboard"])
        tk.Label(self.root, text="User Dashboard", font=("Arial", 18), bg=self.colors["user_dashboard"], fg="white").pack(pady=10)
        tk.Button(self.root, text="View Balance", command=self.view_balance, width=20).pack(pady=5)
        tk.Button(self.root, text="Deposit Money", command=self.deposit, width=20).pack(pady=5)
        tk.Button(self.root, text="Withdraw Money", command=self.withdraw, width=20).pack(pady=5)
        tk.Button(self.root, text="Logout", command=self.main_menu, width=20).pack(pady=10)

    def view_balance(self):
        c.execute("SELECT balance FROM Accounts WHERE user_id=%s", (self.current_user_id,))
        balance = c.fetchone()[0]
        messagebox.showinfo("Balance", f"Your current balance is ₹{balance:.2f}")

    def deposit(self):
        amt = simpledialog.askfloat("Deposit", "Enter amount to deposit:")
        if amt and amt > 0:
            c.execute("UPDATE Accounts SET balance = balance + %s WHERE user_id=%s", (amt, self.current_user_id))
            c.execute("INSERT INTO Transactions (account_id, transaction_type, amount, description) VALUES ((SELECT account_id FROM Accounts WHERE user_id=%s), 'Deposit', %s, %s)",
                      (self.current_user_id, amt, "Deposit by user"))
            conn.commit()
            messagebox.showinfo("Success", "Amount deposited successfully.")

    def withdraw(self):
        amt = simpledialog.askfloat("Withdraw", "Enter amount to withdraw:")
        if amt and amt > 0:
            c.execute("SELECT balance FROM Accounts WHERE user_id=%s", (self.current_user_id,))
            balance = c.fetchone()[0]
            if amt > balance:
                messagebox.showerror("Error", "Insufficient balance.")
                return
            c.execute("UPDATE Accounts SET balance = balance - %s WHERE user_id=%s", (amt, self.current_user_id))
            c.execute("INSERT INTO Transactions (account_id, transaction_type, amount, description) VALUES ((SELECT account_id FROM Accounts WHERE user_id=%s), 'Withdrawal', %s, %s)",
                      (self.current_user_id, amt, "Withdrawal by user"))
            conn.commit()
            messagebox.showinfo("Success", "Amount withdrawn successfully.")

    def admin_login(self):
        self.clear_frame(self.colors["admin_login"])
        tk.Label(self.root, text="Admin Login", font=("Arial", 18), bg=self.colors["admin_login"], fg="white").pack(pady=10)

        user_entry = tk.Entry(self.root)
        pass_entry = tk.Entry(self.root, show="*")

        tk.Label(self.root, text="Username", bg=self.colors["admin_login"], fg="white").pack()
        user_entry.pack()
        tk.Label(self.root, text="Password", bg=self.colors["admin_login"], fg="white").pack()
        pass_entry.pack()

        def login():
            c.execute("SELECT * FROM Admins WHERE username=%s AND password=%s",
                      (user_entry.get(), pass_entry.get()))
            if c.fetchone():
                self.admin_dashboard()
            else:
                messagebox.showerror("Error", "Invalid admin credentials")

        tk.Button(self.root, text="Login", command=login).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.main_menu).pack()

    def admin_dashboard(self):
        self.clear_frame(self.colors["admin_dashboard"])
        tk.Label(self.root, text="Admin Dashboard", font=("Arial", 18), bg=self.colors["admin_dashboard"], fg="white").pack(pady=10)
        tk.Button(self.root, text="View Users", command=self.view_users, width=20).pack(pady=5)
        tk.Button(self.root, text="View Transactions", command=self.view_transactions, width=20).pack(pady=5)
        tk.Button(self.root, text="Add User", command=lambda: self.register_user(return_to_admin=True), width=20).pack(pady=5)
        tk.Button(self.root, text="Remove User", command=self.remove_user_prompt, width=20).pack(pady=5)
        tk.Button(self.root, text="Logout", command=self.main_menu, width=20).pack(pady=10)

    def view_users(self):
        self.clear_frame(self.colors["admin_dashboard"])
        tk.Label(self.root, text="Registered Users", font=("Arial", 16), bg=self.colors["admin_dashboard"], fg="white").pack(pady=10)
        c.execute("SELECT user_id, name, email FROM Users")
        users = c.fetchall()
        for user in users:
            user_frame = tk.Frame(self.root, bg=self.colors["admin_dashboard"])
            user_frame.pack(pady=2)
            tk.Label(user_frame, text=f"{user[0]} - {user[1]} ({user[2]})", bg=self.colors["admin_dashboard"], fg="white").pack(side=tk.LEFT)
            tk.Button(user_frame, text="Delete", command=lambda uid=user[0]: self.remove_user(uid)).pack(side=tk.RIGHT)
        tk.Button(self.root, text="Back", command=self.admin_dashboard).pack(pady=10)

    def remove_user_prompt(self):
        uid = simpledialog.askinteger("Remove User", "Enter User ID to remove:")
        if uid:
            self.remove_user(uid)

    def remove_user(self, user_id):
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete user ID {user_id}?")
        if confirm:
            c.execute("DELETE FROM Transactions WHERE account_id IN (SELECT account_id FROM Accounts WHERE user_id=%s)", (user_id,))
            c.execute("DELETE FROM Accounts WHERE user_id=%s", (user_id,))
            c.execute("DELETE FROM Users WHERE user_id=%s", (user_id,))
            conn.commit()
            messagebox.showinfo("Deleted", f"User ID {user_id} and related records have been deleted.")
            self.view_users()

    def view_transactions(self):
        c.execute("SELECT account_id, transaction_type, amount, transaction_date FROM Transactions")
        txns = c.fetchall()
        info = "\n".join([f"{t[0]} | {t[1]} ₹{t[2]} on {t[3]}" for t in txns]) if txns else "No transactions available."
        messagebox.showinfo("Transactions", info)


if __name__ == "__main__":
    root = tk.Tk()
    app = BankingApp(root)
    root.mainloop()