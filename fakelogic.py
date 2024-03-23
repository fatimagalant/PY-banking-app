import random
import string

def generate_password(length=12):
    # Define character sets for each category
    lowercase_letters = string.ascii_lowercase
    uppercase_letters = string.ascii_uppercase
    digits = string.digits
    symbols = string.punctuation

    # Combine all character sets
    all_characters = lowercase_letters + uppercase_letters + digits + symbols

    # Generate password by randomly selecting characters from all_characters
    password = ''.join(random.choice(all_characters) for _ in range(length))
    
    return password

def main():
    password = generate_password()
    print(password)

if __name__ == "__main__":
    main()
