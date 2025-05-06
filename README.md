
# **Password Manager Web App**

## **Overview:**
This project is a secure web application that allows users to store, retrieve, and manage their passwords for different websites. Built using Flask and SQLite, it includes functionality for encryption, password generation, and user authentication.

The application securely stores passwords in an encrypted form, uses a randomly generated encryption key for each password, and allows users to add, update, retrieve, and delete stored passwords. It also provides a password generator with customizable parameters for creating strong passwords.

## **Features:**
- **User Registration & Login**: Users can create an account, log in, and manage their password vault.
- **Password Management**: Securely save, update, and delete passwords for different websites.
- **Password Generation**: Generate strong, random passwords with a mix of letters, numbers, and special characters.
- **Encryption**: User passwords are encrypted using the Fernet symmetric encryption algorithm to ensure security.
- **Session Management**: Users must be logged in to access and manage their passwords.

## **How It Works:**

1. **User Registration & Login**:
   - Users can create an account by providing a name, email, and password.
   - During login, the system checks if the provided email and password match a registered user in the database.
   
2. **Password Encryption & Decryption**:
   - Passwords are encrypted before being stored in the database using a unique encryption key generated for each password.
   - When retrieving a password, it is decrypted using the corresponding key.

3. **Password Generation**:
   - Users can generate a secure password with random letters, numbers, and symbols by calling the password generation endpoint.

4. **Password Management**:
   - Users can save, update, and delete passwords associated with specific websites.
   - Each password is encrypted using Fernet, and the keys are stored in a separate database.

5. **Database Setup**:
   - SQLite is used to store user data (`users.db`), passwords (`passwords.db`), and encryption keys (`keys.db`).

6. **Session Handling**:
   - The application uses Flask's session management to ensure that only authenticated users can interact with their stored passwords.

## **Endpoints:**

- **`/signup`**: User registration page.
- **`/login`**: User login page.
- **`/logout`**: Logout endpoint.
- **`/generate_password`**: Generates a random password.
- **`/save_password`**: Endpoint for saving passwords.
- **`/get_passwords`**: Retrieve all stored passwords for the logged-in user.
- **`/delete_password/<int:id>`**: Delete a password by ID.
- **`/update_password/<int:id>`**: Update password details for a specific ID.
- **`/decrypt_password/<int:password_id>`**: Decrypt a password by ID and return it in plaintext.

## **Example Usage:**

### 1. **User Registration:**
- When the user accesses the signup page (`/signup`), they will be prompted to provide their name, email, and password. If the user already exists, they will be notified.
  
### 2. **User Login:**
- After registration, users can log in using their credentials. Once logged in, the user can manage their passwords.

### 3. **Adding Passwords:**
- Users can save passwords for different websites. For example, to add a password for "example.com":
  
```

POST /save\_password
{
"website": "example.com",
"email": "[user@example.com](mailto:user@example.com)",
"password": "StrongPassword123!"
}

```

The password will be encrypted and stored in the database.

### 4. **Getting Stored Passwords:**
- To view the stored passwords for the logged-in user:

```

GET /get\_passwords

```

This will return a list of websites and corresponding encrypted passwords.

### 5. **Decrypting a Password:**
- To decrypt a specific password, use:

```

GET /decrypt\_password/\<password\_id>

```

The password will be decrypted and returned in plaintext.

### 6. **Generating a Password:**
- To generate a random password, users can visit:

```

GET /generate\_password

```

This will return a new password with random characters, numbers, and symbols.

## **Requirements:**

- **Python 3.x**
- **Flask**
- **SQLite** (for database management)
- **Cryptography** (for encryption)
- **Pandas** (for CSV file handling)

To install the required dependencies, run:
```

pip install flask cryptography pandas

```

## **File Structure:**
```

password\_manager/
├── app.py               # Main application file
├── templates/
│   ├── index.html       # Home page template
│   ├── login.html       # Login page template
│   └── signup.html      # Signup page template
├── users.db            # SQLite database for users
├── passwords.db        # SQLite database for passwords
├── keys.db             # SQLite database for encryption keys
├── users.csv           # CSV file for storing users
├── passwords.csv       # CSV file for storing passwords
├── keys.csv            # CSV file for storing keys
└── README.md           # Project documentation

```
