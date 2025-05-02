import sqlite3
import pandas as pd
import os
from random import choice, randint, shuffle
import string

# Function to generate random passwords
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

# Create users.db and passwords.db
def create_databases():
    # Create users.db
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        user_email TEXT PRIMARY KEY,
                        user_password TEXT NOT NULL,
                        user_name TEXT NOT NULL)''')
    conn.commit()
    conn.close()

    # Create passwords.db
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

# Save data to CSV and TXT files (append mode)
def save_data_to_csv_and_txt(passwords_data):
    # Convert the list to a pandas DataFrame
    df = pd.DataFrame(passwords_data, columns=["Website", "Email", "Password", "User Email"])
    
    # Check if the CSV file exists
    file_exists = os.path.isfile("passwords.csv")
    
    # Save to CSV (append mode, without writing the header again)
    with open("passwords.csv", 'a', newline='') as file:
        df.to_csv(file, header=not file_exists, index=False)
    
    # Save to TXT (append mode)
    with open("passwords.txt", "a") as file:
        for row in passwords_data:
            file.write(f"Website: {row[0]}, Email: {row[1]}, Password: {row[2]}, User Email: {row[3]}\n")

# Save password to the database
def save_password_to_db(website, email, password, user_email):
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO passwords (website, email, password, user_email)
                      VALUES (?, ?, ?, ?)''', (website, email, password, user_email))
    conn.commit()
    conn.close()

# Save user to the database
def save_user_to_db(name, email, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO users (user_email, user_password, user_name)
                      VALUES (?, ?, ?)''', (email, password, name))
    conn.commit()
    conn.close()

# Function to get user input, create the user, and save the user and password data
def user_signup():
    name = input("Enter your name: ")
    email = input("Enter your email: ")
    password = input("Enter your password: ")

    # Save user to the database
    save_user_to_db(name, email, password)

    # Generate random password for a website (for demo purposes)
    website = "random-website.com"
    generated_password = generate_password()

    # Save password data to the database
    save_password_to_db(website, email, generated_password, email)

    # Prepare data to save to CSV and TXT files
    passwords_data = [
        (website, email, generated_password, email)
    ]
    
    # Save data to CSV and TXT files
    save_data_to_csv_and_txt(passwords_data)

    print(f"User {name} created successfully!")
    print(f"Password for website {website} generated: {generated_password}")

if __name__ == "__main__":
    create_databases()  # Create the databases and tables
    user_signup()  # Execute user signup and data storage
