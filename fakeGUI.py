import tkinter as tk
from tkinter import messagebox, simpledialog
import os
import hashlib
import random
import string
import pyperclip

class BankApplicationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Bank Application")
        self.root.geometry("500x500")

        self.bank_data_folder = "Bank_Data"
        self.current_user_file = None
        self.current_username = None
        self.current_pin = None

        self.create_widgets()

    def create_widgets(self):
        # Labels
        self.label_username = tk.Label(self.root, text="Username:")
        self.label_username.pack()

        self.entry_username = tk.Entry(self.root)
        self.entry_username.pack()

        self.label_pin = tk.Label(self.root, text="Password:")
        self.label_pin.pack()

        self.entry_pin = tk.Entry(self.root, show="*")
        self.entry_pin.pack()

        self.btn_register = tk.Button(self.root, text="Register", command=self.register)
        self.btn_register.pack()

        self.btn_login = tk.Button(self.root, text="Login", command=self.login)
        self.btn_login.pack()

        self.btn_generate_password = tk.Button(self.root, text="Generate Password", command=self.generate_password)
        self.btn_generate_password.pack()

        self.btn_copy_password = tk.Button(self.root, text="Copy Password", command=self.copy_password)
        self.btn_copy_password.pack()

    def register(self):
        username = self.entry_username.get()
        password = self.entry_pin.get()

        if not username or not password:
            messagebox.showerror("Error", "Please provide both username and password.")
            return

        if not os.path.exists(self.bank_data_folder):
            os.makedirs(self.bank_data_folder)

        user_file_path = f"{self.bank_data_folder}/{username}_Data.txt"

        if os.path.exists(user_file_path):
            messagebox.showerror("Error", "Username already exists. Please choose another.")
            return

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        with open(user_file_path, "w") as file:
            file.write(f"{hashed_password}\n")
            file.write("0.0\n")  # Initial balance

        messagebox.showinfo("Success", "Account registered successfully.")

    def login(self):
        username = self.entry_username.get()
        password = self.entry_pin.get()

        user_file_path = f"{self.bank_data_folder}/{username}_Data.txt"

        if not os.path.exists(user_file_path):
            messagebox.showerror("Error", "Account not found. Please register first.")
            return

        with open(user_file_path, "r") as file:
            saved_hashed_password = file.readline().strip()
            entered_hashed_password = hashlib.sha256(password.encode()).hexdigest()
            if saved_hashed_password != entered_hashed_password:
                messagebox.showerror("Error", "Incorrect password.")
                return

        self.current_user_file = user_file_path
        self.current_username = username
        self.show_logged_in_screen()

    def show_logged_in_screen(self):
        self.root.withdraw()  # Hide login screen

        logged_in_window = tk.Toplevel(self.root)
        logged_in_window.title("Logged In")

        btn_balance = tk.Button(logged_in_window, text="Check Balance", command=self.check_balance)
        btn_balance.pack()

        btn_deposit = tk.Button(logged_in_window, text="Deposit", command=self.deposit)
        btn_deposit.pack()

        btn_withdraw = tk.Button(logged_in_window, text="Withdraw", command=self.withdraw)
        btn_withdraw.pack()

        btn_transaction_details = tk.Button(logged_in_window, text="Transaction Details", command=self.show_transaction_details)
        btn_transaction_details.pack()

        btn_logout = tk.Button(logged_in_window, text="Logout", command=self.logout)
        btn_logout.pack()

    def check_balance(self):
        with open(self.current_user_file, "r") as file:
            lines = file.readlines()
            balance = float(lines[1])
            messagebox.showinfo("Balance", f"Your current balance is: {balance}")

    def deposit(self):
        amount = float(tk.simpledialog.askstring("Deposit", "Enter amount to deposit:"))

        if amount <= 0:
            messagebox.showerror("Error", "Amount must be greater than 0.")
            return

        with open(self.current_user_file, "r+") as file:
            lines = file.readlines()
            balance = float(lines[1])
            balance += amount
            file.seek(0)
            file.write(lines[0])
            file.write(f"{balance}\n")

        messagebox.showinfo("Success", "Amount deposited successfully.")

    def withdraw(self):
        amount = float(tk.simpledialog.askstring("Withdraw", "Enter amount to withdraw:"))

        with open(self.current_user_file, "r+") as file:
            lines = file.readlines()
            balance = float(lines[1])

            if amount > balance:
                messagebox.showerror("Error", "Insufficient balance.")
                return

            balance -= amount
            file.seek(0)
            file.write(lines[0])
            file.write(f"{balance}\n")

        messagebox.showinfo("Success", "Amount withdrawn successfully.")

    def show_transaction_details(self):
        with open(self.current_user_file, "r") as file:
            lines = file.readlines()
            transactions = lines[2:]
            message = "\n".join(transactions)
            messagebox.showinfo("Transaction Details", message)

    def logout(self):
        self.root.deiconify()  # Show login screen
        self.current_user_file = None
        self.current_username = None
        self.current_pin = None

    def generate_password(self):
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        self.entry_pin.delete(0, tk.END)
        self.entry_pin.insert(0, password)

    def copy_password(self):
        password = self.entry_pin.get()
        pyperclip.copy(password)
        messagebox.showinfo("Success", "Password copied to clipboard.")

if __name__ == "__main__":
    root = tk.Tk()
    app = BankApplicationGUI(root)
    root.mainloop()
