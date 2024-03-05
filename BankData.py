# Python program to create Bankaccount class
# with both a deposit() and a withdraw() function
class Bank_Account:
	user_input = input('(y/n)')
	yes_choice = ['yes', 'y']
	no_choice = ['no', 'n']
	def __init__(self):
		self.balance=0
		print("Hello!!! Welcome to D&W Bank. Would you like to make a transaction ?")
	def deposit(self):
		amount=float(input("How much would you like to deposit?"))
		if (amount>0):
			self.balance += amount
			print("\n Amount Deposited:",amount)
		else: 
			print('Please enter a valid amount')

	def withdraw(self):
		amount = float(input("How much would you like to withdraw?"))
		if self.balance>=amount:
			self.balance-=amount
			print("\n You Withdrew:", amount)
		else:
			print("\n Insufficient balance ")

	def display(self):
		print("\n Net Available Balance=",self.balance)

# Driver code

# creating an object of class
s = Bank_Account()

# Calling functions with that class object
s.deposit()
s.withdraw()
s.display()
