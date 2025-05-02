from tkinter import * 
from tkinter import messagebox  
from random import choice, randint, shuffle
import sqlite3
import re
import pandas as pd
import pyperclip
import os
from cryptography.fernet import Fernet 

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    """
    Generates a random password that includes a mix of letters, numbers, and symbols.
    - Password length: 10 to 16 letters
    - Symbol count: 2 to 4 symbols
    - Number count: 2 to 4 numbers
    The generated password is displayed in the password entry field and copied to the clipboard.
    """
    # Clear the password entry 
    password_entry.delete(0, END)
    # Define character sets for password generation

    small_letters  = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z']
    capital_letters=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    # Generate random sections for the password using list comprehension
    # worst case the password is 10 char long
    password_capital_letters = [choice(small_letters) for _ in range(randint(3, 4))]
    password_small_letters = [choice(capital_letters) for _ in range(randint(3, 4))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_capital_letters + password_symbols + password_numbers + password_small_letters
    shuffle(password_list)

    # Join the list of characters into a single string to form the password
    password = "".join(password_list)
    # Insert the generated password into the password entry field
    password_entry.insert(0, password)
    # Copy the generated password to the clipboard
    pyperclip.copy(password)
   
# ---------------------------- ENCRYPTION ------------------------------- #
""" 
# key is generated 
global key
key = Fernet.generate_key() 

# value of key is assigned to a variable 
global f
f = Fernet(key) 

global token

def encryption(password):
    
    password=password.encode()
    encrypted_bytes = f.encrypt(password)
    encrypted_bytes=encrypted_bytes.decode('utf-8')
    return encrypted_bytes
"""


# ---------------------------- DECRYPTION ------------------------------- #
""" 
def DECRYPTION(encrypted_password):
    encrypted_password=encrypted_password.encode('utf-8')
    decrypted_bytes = f.decrypt(encrypted_password)
    decrypted_bytes=decrypted_bytes.decode('utf-8')
    return decrypted_bytes

"""
# ---------------------------- INPUT VALIDATION ------------------------------- #


def email_validation(test):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if re.match(pattern, test):
        return True
    else:
        messagebox.showinfo(title="Invalid Email", message="Please enter a valid email. Like email@gmail.com")
        return False
    


def password_validation(password):
    min_length = 8
    valid = True

    if len(password) < min_length:
        messagebox.showinfo(title="Invalid Password", message="Password must be at least 8 characters long.")
        valid = False
    elif not re.search(r"\d", password):
        messagebox.showinfo(title="Invalid Password", message="Password must contain at least one digit.")
        valid = False
    elif not re.search(r"[A-Z]", password):
        messagebox.showinfo(title="Invalid Password", message="Password must contain at least one uppercase letter.")
        valid = False
    elif not re.search(r"[a-z]", password):
        messagebox.showinfo(title="Invalid Password", message="Password must contain at least one lowercase letter.")
        valid = False
    elif not re.search(r"[!#$%&()*+]", password):
        messagebox.showinfo(title="Invalid Password", message="Password must contain at least one special character like these # $ % &")
        valid = False

    return valid


# ---------------------------- SAVE PASSWORD ------------------------------- #

def save():

    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    # Check if website and password fields are empty
    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty.")

    # Input validations
    elif not email_validation(email) : 
        return  

    elif not password_validation(password):
        return


    else:

        # password_encrypted=encryption(password)
        # Show a confirmation dialog before saving the data
        is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered: \nEmail: {email} "
                                                      f"\nPassword: {password} \nIs it ok to save?")
        if is_ok:
            # Append the data to the 'data.txt' file

            with open("password.txt", "a") as data_file:
                data_file.write(f"{website} | {email} | {password}\n")
                # Clear the entry fields after saving

            ## save to csv
            new_entry = {
                'Website': [website],
                'Email': [email],
                'Password': [password]
            }

            # Convert to DataFrame
            new_df = pd.DataFrame(new_entry)

            # Append to existing CSV or create new file
            if os.path.exists('passwords.csv'):
                existing_df = pd.read_csv('passwords.csv')
                updated_df = pd.concat([existing_df, new_df], ignore_index=True)
            else:
                updated_df = new_df

            updated_df.to_csv('passwords.csv', index=False)

            # Save to db
            # Connect to SQLite database (it will be created if it doesn't exist)
            conn = sqlite3.connect('passwords.db')
            cursor = conn.cursor()
            
            # Create table if it doesn't exist
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS passwords (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    website TEXT NOT NULL,
                    email TEXT NOT NULL,
                    password TEXT NOT NULL
                )
            ''')
            
            # Insert the new entry
            cursor.execute('''
                INSERT INTO passwords (website, email, password)
                VALUES (?, ?, ?)
            ''', (website, email, password))
            
            # Commit changes and close connection
            conn.commit()
            conn.close()

            # Clear the entry fields after saving
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")  
window.config(padx=50, pady=50)  



canvas = Canvas(height=200, width=200)
logo_img = PhotoImage(file="logo.png")  
canvas.create_image(100, 100, image=logo_img)  
canvas.grid(row=0, column=1)  


website_label = Label(text="Website:")
website_label.grid(row=1, column=0)  

email_label = Label(text="Email:")
email_label.grid(row=2, column=0)  

password_label = Label(text="Password:")
password_label.grid(row=3, column=0)  

website_entry = Entry(width=35)
website_entry.grid(row=1, column=1, columnspan=2)  
website_entry.focus()  # Focus on the website entry field when the window is opened

email_entry = Entry(width=35)
email_entry.grid(row=2, column=1, columnspan=2)  
email_entry.insert(0, "example@gmail.com")  

password_entry = Entry(width=35)
password_entry.grid(row=3, column=1,columnspan=2)  

generate_password_button = Button(text="Generate Password", command=generate_password)
generate_password_button.grid(row=3, column=2)  

add_button = Button(text="Add", width=36, command=save)
add_button.grid(row=4, column=1, columnspan=2)  

window.mainloop()
