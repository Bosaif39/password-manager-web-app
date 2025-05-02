from flask import Flask, render_template, request, jsonify
from random import choice, randint, shuffle
import sqlite3
import re
import pyperclip

app = Flask(__name__)

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    """
    Generates a random password that includes a mix of letters, numbers, and symbols.
    - Password length: 10 to 16 letters
    - Symbol count: 2 to 4 symbols
    - Number count: 2 to 4 numbers
    The generated password is copied to the clipboard and returned.
    """
    small_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    capital_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_small_letters = [choice(small_letters) for _ in range(randint(3, 4))]
    password_capital_letters = [choice(capital_letters) for _ in range(randint(3, 4))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_small_letters + password_capital_letters + password_symbols + password_numbers
    shuffle(password_list)
    
    password = "".join(password_list)
    pyperclip.copy(password)
    
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
    if not re.search(r"[!#$%&()*+]", password):
        return False
    return True

# ---------------------------- DATABASE SETUP ------------------------------- #
def init_db():
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS passwords (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        website TEXT NOT NULL,
                        email TEXT NOT NULL,
                        password TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password(website, email, password):
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO passwords (website, email, password)
                      VALUES (?, ?, ?)''', (website, email, password))
    conn.commit()
    conn.close()

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
    website = request.json.get('website')
    email = request.json.get('email')
    password = request.json.get('password')
    
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()
    cursor.execute('''UPDATE passwords SET website = ?, email = ?, password = ? WHERE id = ?''',
                   (website, email, password, id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Password updated successfully!"})

# ---------------------------- ROUTES ------------------------------- #

@app.route('/')
def index():
    return render_template('index.html')


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
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, website, email, password FROM passwords")
    rows = cursor.fetchall()
    conn.close()
    
    data = [
        {"id": row[0], "website": row[1], "email": row[2], "password": row[3]}
        for row in rows
    ]
    return jsonify(data)


if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(debug=True)
