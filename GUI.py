import tkinter as tk
from tkinter import messagebox
import random
import hashlib
import pyperclip

class BankLogin:
    def __init__(self, master):
        self.master = master
        self.master.title("Bank Account Login")

        self.username_label = tk.Label(master, text="Username:")
        self.username_entry = tk.Entry(master)
        self.password_label = tk.Label(master, text="Password:")
        self.password_entry = tk.Entry(master, show="*")
        self.generate_password_button = tk.Button(master, text="Generate Password", command=self.generate_password)
        self.hash_password_button = tk.Button(master, text="Hash Password", command=self.hash_password)
        self.copy_password_button = tk.Button(master, text="Copy Password", command=self.copy_password)
        self.login_button = tk.Button(master, text="Login", command=self.login)

        self.username_label.grid(row=0, column=0, sticky="e")
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)
        self.password_label.grid(row=1, column=0, sticky="e")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)
        self.generate_password_button.grid(row=1, column=2, padx=5, pady=5)
        self.hash_password_button.grid(row=2, column=1, padx=5, pady=5)
        self.copy_password_button.grid(row=2, column=2, padx=5, pady=5)
        self.login_button.grid(row=3, columnspan=2, pady=10)

    def generate_password(self):
        # Generate a random password of length 8
        password = ''.join(random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for i in range(8))
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)

    def hash_password(self):
        password = self.password_entry.get()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, hashed_password)

    def copy_password(self):
        password = self.password_entry.get()
        pyperclip.copy(password)
        messagebox.showinfo("Password Copied", "Password has been copied to clipboard.")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Here you would validate the username and password against your backend data
        # For demonstration, let's just print the entered credentials
        print("Username:", username)
        print("Password:", password)

        # You can implement your authentication logic here

def main():
    root = tk.Tk()
    app = BankLogin(root)
    root.mainloop()

if __name__ == "__main__":
    main()
