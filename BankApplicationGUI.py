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
        self.transaction_folder = "Transaction_Data"
        self.current_user_folder = None
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

        self.label_balance = tk.Label(self.root, text="Opening Balance:")
        self.label_balance.pack()

        self.entry_balance = tk.Entry(self.root)
        self.entry_balance.pack()

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
        opening_balance = self.entry_balance.get()

        if not username or not password or not opening_balance:
            messagebox.showerror("Error", "Please provide username, password, and opening balance.")
            return

        if not opening_balance.isdigit():
            messagebox.showerror("Error", "Opening balance must be a numeric value.")
            return

        if not os.path.exists(self.bank_data_folder):
            os.makedirs(self.bank_data_folder)

        user_folder_path = os.path.join(self.bank_data_folder, username)
        user_file_path = os.path.join(user_folder_path, f"{username}_Data.txt")

        if os.path.exists(user_folder_path):
            messagebox.showerror("Error", "Username already exists. Please choose another.")
            return

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        os.makedirs(user_folder_path)

        with open(user_file_path, "w") as file:
            file.write(f"Username: {username}\n")
            file.write(f"Password: {hashed_password}\n")
            file.write(f"Balance: {float(opening_balance):.2f}\n")  # Opening balance

        # Create transaction folder for the user
        transaction_folder_path = os.path.join(self.transaction_folder, username)
        os.makedirs(transaction_folder_path)

        messagebox.showinfo("Success", "Account registered successfully.")

    def login(self):
        username = self.entry_username.get()
        password = self.entry_pin.get()

        user_file_path = os.path.join(self.bank_data_folder, f"{username}/{username}_Data.txt")

        if not os.path.exists(user_file_path):
            messagebox.showerror("Error", "Account not found. Please register first.")
            return

        with open(user_file_path, "r") as file:
            lines = file.readlines()
            saved_hashed_password = lines[1].split(":")[1].strip()  # Extracting hashed password from the file
            entered_hashed_password = hashlib.sha256(password.encode()).hexdigest()
            if saved_hashed_password != entered_hashed_password:
                messagebox.showerror("Error", "Incorrect password.")
                return

        self.current_user_folder = os.path.dirname(user_file_path)
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
            balance = float(lines[2].split(":")[1].strip())  # Extracting balance from the file
            messagebox.showinfo("Balance", f"Your current balance is: {balance}")

    def deposit(self):
        amount = float(tk.simpledialog.askstring("Deposit", "Enter amount to deposit:"))

        if amount <= 0:
            messagebox.showerror("Error", "Amount must be greater than 0.")
            return

        with open(self.current_user_file, "r+") as file:
            lines = file.readlines()
            balance = float(lines[2].split(":")[1].strip())  # Extracting balance from the file
            balance += amount
            file.seek(0)
            file.write(lines[0])
            file.write(lines[1])
            file.write(f"Balance: {balance:.2f}\n")

        # Record transaction
        transaction_amount = f"+{amount:.2f}"
        self.record_transaction(transaction_amount)

        messagebox.showinfo("Success", "Amount deposited successfully.")

    def withdraw(self):
        amount = float(tk.simpledialog.askstring("Withdraw", "Enter amount to withdraw:"))

        with open(self.current_user_file, "r+") as file:
            lines = file.readlines()
            balance = float(lines[2].split(":")[1].strip())  # Extracting balance from the file

            if amount > balance:
                messagebox.showerror("Error", "Insufficient balance.")
                return

            balance -= amount
            file.seek(0)
            file.write(lines[0])
            file.write(lines[1])
            file.write(f"Balance: {balance:.2f}\n")

        # Record transaction
        transaction_amount = f"-{amount:.2f}"
        self.record_transaction(transaction_amount)

        messagebox.showinfo("Success", "Amount withdrawn successfully.")

    def show_transaction_details(self):
        transaction_folder_path = os.path.join(self.transaction_folder, self.current_username)
        transaction_files = os.listdir(transaction_folder_path)

        if not transaction_files:
            messagebox.showinfo("Transaction Details", "No transactions yet.")
            return

        transactions = ""
        for file_name in transaction_files:
            file_path = os.path.join(transaction_folder_path, file_name)
            with open(file_path, "r") as file:
                transaction_data                = file.read()
                transactions += f"{transaction_data}\n"

        messagebox.showinfo("Transaction Details", transactions)

    def logout(self):
        self.root.deiconify()  # Show login screen
        self.clear_login_details()

    def clear_login_details(self):
        self.entry_username.delete(0, tk.END)
        self.entry_pin.delete(0, tk.END)
        self.entry_balance.delete(0, tk.END)
        self.current_user_folder = None
        self.current_user_file = None
        self.current_username = None
        self.current_pin = None

    def record_transaction(self, transaction_amount):
        transaction_folder_path = os.path.join(self.transaction_folder, self.current_username)
        transaction_file = os.path.join(transaction_folder_path, f"{self.current_username}_Transaction.txt")

        with open(transaction_file, "a") as file:
            file.write(f"{transaction_amount}\n")

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
