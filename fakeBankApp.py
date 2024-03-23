import os

class fakeBank():
    def load_balance():
        try:
            with open("Bank Data.txt", "r") as file:
                balance = float(file.read().strip())
        except FileNotFoundError:
            balance = 0.0
        return balance

def update_balance(amount):
    balance = load_balance()
    balance += amount
    with open("Bank Data.txt", "w") as file:
        file.write(str(balance))

def log_transaction(transaction_type, amount):
    with open("Transaction Log.txt", "a") as file:
        file.write(f"{transaction_type}: {amount}\n")

def make_transaction():
    while True:
        choice = input("Would you like to make a transaction? (Yes/No): ").strip().lower()
        if choice == "yes":
            return True
        elif choice == "no":
            return False
        else:
            print("You provided an invalid input.")

def deposit_or_withdraw():
    while True:
        choice = input("Would you like to make a deposit or withdrawal? (Deposit/Withdraw): ").strip().lower()
        if choice == "deposit":
            return True
        elif choice == "withdraw":
            return False
        else:
            print("You provided an invalid input.")

def get_transaction_amount():
    while True:
        try:
            amount = float(input("How much would you like to deposit or withdraw? "))
            return amount
        except ValueError:
            print("You provided an invalid input.")

def main():
    while True:
        if make_transaction():
            current_balance = load_balance()
            print(f"Current Balance: ${current_balance}")
            if deposit_or_withdraw():
                amount = get_transaction_amount()
                update_balance(amount)
                log_transaction("Deposit", amount)
            else:
                amount = get_transaction_amount()
                if amount > current_balance:
                    print("Insufficient funds.")
                else:
                    update_balance(-amount)
                    log_transaction("Withdrawal", amount)
            current_balance = load_balance()
            print(f"Current Balance: ${current_balance}")
        else:
            break

if __name__ == "__main__":
    bank_app = fakeBankApp()
    bank_app.run()
    # main()
