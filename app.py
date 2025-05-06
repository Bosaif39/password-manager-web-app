from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from random import choice, randint, shuffle
import sqlite3
import re
import os
import pandas as pd
import string
from cryptography.fernet import Fernet 

app = Flask(__name__)
app.secret_key = 'myDude'

global key
key = Fernet.generate_key() 
global f
f = Fernet(key) 
global token

# ---------------------------- ENCRYPTION ------------------------------- #

def encryption(password,f):
    password=password.encode()
    encrypted_bytes = f.encrypt(password)
    encrypted_bytes = encrypted_bytes.decode('utf-8')
    return encrypted_bytes


# ---------------------------- DECRYPTION ------------------------------- #
def decryption(encrypted_password, f):
    encrypted_password = encrypted_password.strip()
    encrypted_password = encrypted_password.encode('utf-8')
    decrypted_bytes = f.decrypt(encrypted_password)
    decrypted_bytes = decrypted_bytes.decode('utf-8')
    return decrypted_bytes



# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    """
    Generates a random password that includes a mix of letters, numbers, and symbols.
    - Password length: 10 to 16 letters
    - Symbol count: 2 to 4 symbols
    - Number count: 2 to 4 numbers
    The generated password is copied to the clipboard and returned.
    """
    small_letters = string.ascii_lowercase
    capital_letters = string.ascii_uppercase
    numbers = string.digits
    
    symbols = ['!', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/',
                ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~'] 

    password_small_letters = [choice(small_letters) for _ in range(randint(3, 4))]
    password_capital_letters = [choice(capital_letters) for _ in range(randint(3, 4))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_small_letters + password_capital_letters + password_symbols + password_numbers
    shuffle(password_list)
    
    password = "".join(password_list)
    
    return password

# ---------------------------- EMAIL VALIDATION ------------------------------- #
def email_validation(test):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, test) is not None

# ---------------------------- PASSWORD VALIDATION ------------------------------- #
def password_validation(password):
    if len(password) < 8:
        return False
    if not re.search(r"\d", password): 
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    
    
    if not re.search(r"[!#$%&'()*+,\-./:;<=>?@\[\\\]^_`{|}~]", password):        
        return False
    
    return True

# ---------------------------- DATABASE SETUP ------------------------------- #
def init_db():
    # Initialize the 'users' table
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        user_email TEXT PRIMARY KEY,
                        user_password TEXT NOT NULL,
                        user_name TEXT NOT NULL)''')
    conn.commit()
    conn.close()

    # Initialize the 'passwords' table with a foreign key to 'users'
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS passwords (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        website TEXT NOT NULL,
                        email TEXT NOT NULL,
                        password TEXT NOT NULL,
                        user_email TEXT,
                        FOREIGN KEY (user_email) REFERENCES users(user_email) ON DELETE CASCADE)''')
    conn.commit()
    conn.close()

    

    # Initialize the 'keys' table 
    conn = sqlite3.connect('keys.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS keys (
                        key TEXT PRIMARY KEY,
                        id INTEGER NOT NULL,
                        FOREIGN KEY (id) REFERENCES passwords(id) ON DELETE CASCADE)''')
    conn.commit()
    conn.close()


# ---------------------------- SAVE USER ------------------------------- #



def save_user(name, email, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO users (user_email, user_password, user_name)
                      VALUES (?, ?, ?)''', (email, password, name))
    conn.commit()
    conn.close()

    # Optionally, log this to a text file
    with open("users.txt", "a") as data_file:
        data_file.write(f"{name} | {email} | {password}\n")

    # Save to CSV
    new_entry = {'name': [name], 'Email': [email], 'Password': [password]}

    # Convert to DataFrame
    new_df = pd.DataFrame(new_entry)

    # Append to existing CSV or create a new file
    if os.path.exists('users.csv'):
        existing_df = pd.read_csv('users.csv')
        updated_df = pd.concat([existing_df, new_df], ignore_index=True)
    else:
        updated_df = new_df

    # Save to CSV file
    updated_df.to_csv('users.csv', index=False)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password(website, email, password):
    # Ensure the user is logged in by checking the session
    if 'user' not in session:
        return jsonify({"error": "User not logged in"}), 401  # User must be logged in

    user_email = session['user']  # Get the logged-in user's email

    
    key = Fernet.generate_key()
    f = Fernet(key)
    encrypted_password = encryption(password, f)

    # Insert password into the database, including the user_email
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO passwords (website, email, password, user_email)
                      VALUES (?, ?, ?, ?)''', (website, email, encrypted_password, user_email))
    
    conn.commit()
    password_id = cursor.lastrowid  # Grab the ID here

    # Optionally, log this to a text file
    with open("password.txt", "a") as data_file:
        data_file.write(f"{password_id} | {website} | {email} | {encrypted_password} | {user_email}\n")

    # Save to CSV
    new_entry = {'Website': [website], 'Email': [email], 'Password': [encrypted_password], 'User Email': [user_email]}

    # Convert to DataFrame
    new_df = pd.DataFrame(new_entry)

    # Append to existing CSV or create a new file
    if os.path.exists('passwords.csv'):
        existing_df = pd.read_csv('passwords.csv')
        updated_df = pd.concat([existing_df, new_df], ignore_index=True)
    else:
        updated_df = new_df

    # Save to CSV file
    updated_df.to_csv('passwords.csv', index=False)

    # save to keys.db
    
    conn_keys = sqlite3.connect('keys.db')
    cursor_keys = conn_keys.cursor()
    cursor_keys.execute("INSERT INTO keys (key, id) VALUES (?, ?)", (key.decode(), password_id))
    conn_keys.commit()
    conn_keys.close()

    # Optionally, log this to a text file
    with open("keys.txt", "a") as data_file:
        data_file.write(f"{password_id} | {key.decode()} \n")


    # Save to CSV
    new_entry = {'password_id': [password_id], 'key': [key.decode()]}

    # Convert to DataFrame
    new_df = pd.DataFrame(new_entry)

    # Append to existing CSV or create a new file
    if os.path.exists('keys.csv'):
        existing_df = pd.read_csv('keys.csv')
        updated_df = pd.concat([existing_df, new_df], ignore_index=True)
    else:
        updated_df = new_df

    # Save to CSV file
    updated_df.to_csv('keys.csv', index=False)

    return jsonify({"message": "Password added successfully!"})



# ---------------------------- DELETE PASSWORD ------------------------------- #
@app.route('/delete_password/<int:id>', methods=['DELETE'])
def delete_password(id):
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM passwords WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Password deleted successfully!"})

# ---------------------------- UPDATE PASSWORD ------------------------------- #
@app.route('/update_password/<int:id>', methods=['PUT'])
def update_password(id):
    data = request.get_json()
    website = data.get('website', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '').strip()

    # Fetch current record from DB
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()
    cursor.execute('SELECT website, email, password FROM passwords WHERE id = ?', (id,))

    # Validate fields
    if not website or not email or not password:
        return jsonify({"error": "All fields are required."}), 400

    if not email_validation(email):
        return jsonify({"error": "Invalid email address. Use something like email@gmail.com"}), 400

    if not password_validation(password):
        return jsonify({"error": "Password must be at least 8 characters long, contain a digit, an uppercase letter, a lowercase letter, and a special character (e.g., #, $, %, &)."}), 400

    # Proceed with update
    cursor.execute('UPDATE passwords SET website = ?, email = ?, password = ? WHERE id = ?',
                   (website, email, password, id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Row updated successfully!"})

# ---------------------------- ROUTES ------------------------------- #

# Index ROUTES
@app.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    user_email = session['user']
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT user_name FROM users WHERE user_email = ?', (user_email,))
    user = cursor.fetchone()
    conn.close()
    
    user_name = user[0] if user else "User"

    return render_template('index.html', name=user_name)


@app.route('/generate_password', methods=['GET'])
def generate_password_route():
    password = generate_password()
    return jsonify({"password": password})


@app.route('/save_password', methods=['POST'])
def save_password_route():
    website = request.form['website']
    email = request.form['email']
    password = request.form['password']
    
    if not email_validation(email):
        return jsonify({"error": "Invalid email address. Use something like email@gmail.com"}), 400
    
    if not password_validation(password):
        return jsonify({"error": "Password must be at least 8 characters long, contain a digit, an uppercase letter, a lowercase letter, and a special character (e.g., #, $, %, &)."}), 400
    
    save_password(website, email, password)
    return jsonify({"message": "Password saved successfully!"})


@app.route('/get_passwords', methods=['GET'])
def get_passwords():
    if 'user' not in session:
        return jsonify({"error": "User not logged in"}), 401  # Ensure user is logged in

    user_email = session['user']  

    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()
    
    # Fetch passwords only for the logged-in user
    cursor.execute("SELECT id, website, email, password FROM passwords WHERE user_email = ?", (user_email,))
    rows = cursor.fetchall()
    conn.close()

    data = [
        {"id": row[0], "website": row[1], "email": row[2], "password": row[3]}
        for row in rows
    ]
    
    return jsonify(data)

# Sign up routes

@app.route('/signup', methods=['GET'])
def signup_page():
    return render_template('signup.html')

# Sign up POST Route
@app.route('/signup', methods=['POST'])
def signup():
    data = request.form  # data from the form (not JSON)
    name = data.get('name').strip()
    email = data.get('email').strip()
    password = data.get('password').strip()

    # Validate email
    if not email_validation(email):
        return jsonify({"error": "Invalid email format."}), 400

    # Validate password
    if not password_validation(password):
        return jsonify({"error": "Password must be at least 8 characters long, contain a digit, an uppercase letter, a lowercase letter, and a special character (e.g., #, $, %, &)."}), 400


    # Check if user already exists
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE user_email = ?', (email,))
    existing_user = cursor.fetchone()
    conn.close()

    if existing_user:
        return jsonify({"error": "User with this email already exists."}), 400

    # Save the new user to the database
    save_user(name, email, password)

    return jsonify({"message": "User created successfully!"}), 201



# Login routes

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    # Get JSON data from the request body
    data = request.get_json()

    email = data.get('email').strip()
    password = data.get('password').strip()

    # Make sure that the user provided both email and password
    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    # Connect to the database
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Check if the user exists
    cursor.execute('SELECT * FROM users WHERE user_email = ? AND user_password = ?', (email, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        session['user'] = email  # Mark the user as logged in
        return jsonify({'message': 'Login successful'}), 200  # Return success message
    else:
        return jsonify({'error': 'Invalid email or password'}), 401  # Invalid credentials error

# logout
@app.route('/logout', methods=['GET'])
def logout():
    session.pop('user', None)  # Clear the session
    return jsonify({'message': 'Logged out successfully'}), 200



@app.route('/decrypt_password/<int:password_id>')
def decrypt_password(password_id):
    if 'user' not in session:
        return jsonify({"error": "User not logged in"}), 401

    # Get encrypted password from passwords.db
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM passwords WHERE id = ?", (password_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return jsonify({"error": "Password not found"}), 404

    encrypted_password = row[0]

    # Get key from keys.db
    conn_keys = sqlite3.connect('keys.db')
    cursor_keys = conn_keys.cursor()
    cursor_keys.execute("SELECT key FROM keys WHERE id = ?", (password_id,))
    row_key = cursor_keys.fetchone()
    conn_keys.close()


    if not row_key:
        return jsonify({"error": "Key not found"}), 404

    key = row_key[0].encode('utf-8')
    f = Fernet(key)
    
    print("Encrypted password:", encrypted_password)
    print("Key:", key)


    try:
        decrypted_password = decryption(encrypted_password, f)
    except Exception as e:
        return jsonify({"error": "Decryption failed"}), 500

    return jsonify({"decrypted_password": decrypted_password})



if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(debug=True)
