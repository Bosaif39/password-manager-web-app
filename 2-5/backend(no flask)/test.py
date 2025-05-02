import sqlite3
import pandas as pd
import random
import string
from random import choice, randint, shuffle

# Function to initialize the databases and create the tables
def init_db():
    # Connect to passwords.db and create the table
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS passwords (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        website TEXT NOT NULL,
                        email TEXT NOT NULL,
                        password TEXT NOT NULL,
                        user_email TEXT,
                        FOREIGN KEY (user_email) REFERENCES users(user_email))''')
    conn.commit()
    conn.close()

    # Connect to users.db and create the table
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        user_email TEXT PRIMARY KEY,
                        user_password TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# Function to generate a random password
def generate_password():
    """
    Generates a random password that includes a mix of letters, numbers, and symbols.
    - Password length: 10 to 16 letters
    - Symbol count: 2 to 4 symbols
    - Number count: 2 to 4 numbers
    """
    small_letters = string.ascii_lowercase
    capital_letters = string.ascii_uppercase
    numbers = string.digits
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_small_letters = [choice(small_letters) for _ in range(randint(3, 4))]
    password_capital_letters = [choice(capital_letters) for _ in range(randint(3, 4))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_small_letters + password_capital_letters + password_symbols + password_numbers
    shuffle(password_list)
    
    password = "".join(password_list)
    
    return password

# Function to store user credentials in users.db
def store_user():
    # Collect username and password from the user
    user_email = input("Enter your email: ")
    user_password = input("Enter your password: ")

    # Connect to users.db to store user credentials
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO users (user_email, user_password)
                      VALUES (?, ?)''', (user_email, user_password))
    conn.commit()
    conn.close()

    return user_email

# Function to store generated passwords in passwords.db
def store_passwords(user_email):
    websites = ["example.com", "facebook.com", "twitter.com", "github.com", "linkedin.com"]
    passwords_data = []

    # Generate passwords for different websites and store in passwords.db
    for website in websites:
        password = generate_password()
        email = f"{user_email}@outlook.com"

        # Insert the generated password into passwords.db
        conn = sqlite3.connect('passwords.db')
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO passwords (website, email, password, user_email)
                          VALUES (?, ?, ?, ?)''', (website, email, password, user_email))
        conn.commit()
        conn.close()

        passwords_data.append([website, email, password, user_email])

    return passwords_data

# Function to save data to CSV and TXT files
def save_data_to_csv_and_txt(passwords_data):
    # Convert the list to a pandas DataFrame
    df = pd.DataFrame(passwords_data, columns=["Website", "Email", "Password", "User Email"])
    
    # Save to CSV
    df.to_csv("passwords.csv", index=False)

    # Save to TXT
    with open("passwords.txt", "a") as file:
        for row in passwords_data:
            file.write(f"Website: {row[0]}, Email: {row[1]}, Password: {row[2]}, User Email: {row[3]}\n")

# Main execution
if __name__ == "__main__":
    init_db()  # Initialize the databases
    user_email = store_user()  # Store user in users.db
    passwords_data = store_passwords(user_email)  # Store passwords in passwords.db
    save_data_to_csv_and_txt(passwords_data)  # Save data to CSV and TXT
    print("Data saved successfully!")
