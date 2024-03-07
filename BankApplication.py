import os


class BankApplication:
    def __init__(self):
        self.balance = 0
        self.bank_data_folder = "Bank_Data"
        self.transaction_log_file = None
        self.user_name = None
        self.user_age = None
    def load_balance(self):
        try:
            with open(f"{self.bank_data_folder}/{self.user_name}_Bank_Data.txt", "r") as file:
                self.balance = float(file.readline())
        except FileNotFoundError:
            self.balance = 0  # Set balance to 0 if file doesn't exist for the current user

    def save_balance(self):
        if not os.path.exists(self.bank_data_folder):
            os.makedirs(self.bank_data_folder)
        with open(f"{self.bank_data_folder}/{self.user_name}_Bank_Data.txt", "w") as file:
            file.write(str(self.balance))

    def log_transaction(self, transaction_type, amount):
        with open(self.transaction_log_file, "a") as file:
            file.write(f"{transaction_type}: {amount}\n")

    def display_balance(self):
        print(f"Current Balance: R{self.temp_balance}")

    def deposit(self):
        while True:
            try:
                amount = float(input("How much would you like to deposit? "))
                if amount > 0:
                    self.temp_balance += amount
                    self.log_transaction("Deposit", amount)
                    self.display_balance()
                    break
                else:
                    print("Invalid amount provided. Please enter a positive amount.")
            except ValueError:
                print("Invalid input. Please provide a valid number.")

    def withdraw(self):
        while True:
            try:
                amount = float(input("How much would you like to withdraw? "))
                if 0 < amount <= self.temp_balance:
                    self.temp_balance -= amount
                    self.log_transaction("Withdrawal", amount)
                    self.display_balance()
                    break
                else:
                    print("Insufficient funds or invalid amount provided.")
            except ValueError:
                print("Invalid input. Please provide a valid number.")

    def view_balance(self):
        self.display_balance()

    def run(self):
        print("Welcome to the Bank Application!")
        while True:
            try:
                self.user_name = input("Please enter your name: ").strip()
                self.user_age = int(input("Please enter your age: ").strip())
                if self.user_age >= 16:
                    print(f"Welcome, {self.user_name}!")
                    break  # Break out of the loop if the age is valid
                else:
                    print("Invalid age! Please try again.")
            except ValueError:
                print("Invalid input. Please enter a valid age as a number.")
                self.transaction_log_file = f"{self.user_name}_Transaction_Log.txt"
                self.load_balance()
                print(f"Welcome, {self.user_name}!")
                while True:
                    print("\nMenu:")
                    print("1. Make a transaction")
                    print("2. View current balance")
                    print("3. Save changes")
                    print("4. Exit")
                    choice = input("Please choose an option: ").strip()
                    if choice not in ["1", "2", "3", "4"]:
                        print("Invalid option. Please choose a valid option.")
                        continue

                    if choice == "4":
                        print("Thank you for using the Bank Application. Goodbye!")
                        return

                    if choice == "3":
                        self.balance = self.temp_balance
                        self.save_balance()
                        print("Changes saved.")
                        continue  # Continue the loop without displaying menu options

                    if choice == "1":
                        while True:
                            transaction_choice = input("Would you like to make a transaction? (Yes/No) ").strip().lower()
                            if transaction_choice not in ["y", "n", "yes", "no"]:
                                print("Invalid input. Please enter 'Yes' or 'No'.")
                                continue
                            if transaction_choice == "n" or transaction_choice == "no":
                                print("Thank you for using the Bank Application. Goodbye!")
                                return

                            print("1. Deposit")
                            print("2. Withdraw")
                            transaction_type = input("Choose an option (1/2): ").strip()
                            if transaction_type not in ["1", "2"]:
                                print("Invalid option. Please choose 1 or 2.")
                                continue
                            
                            self.display_balance()

                            if transaction_type == "1":
                                self.deposit()
                            else:
                                self.withdraw()
                            break

                    elif choice == "2":
                        self.load_balance()  # Reload balance to ensure it's up to date
                        self.view_balance()

            except ValueError as e:
                print(f"Error: {str(e)}")

# Main program
if __name__ == "__main__":
    bank_app = BankApplication()
    bank_app.run()
