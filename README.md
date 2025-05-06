
# Password Manager

## Overview

This project is a simple password manager that allows you to securely manage passwords, including signing up, logging in, and managing your credentials for different websites. The app helps you store passwords securely, retrieve them, and generate random passwords.

## Features

* **Sign Up**: Users can create an account with a name, email, and password.
* **Login**: Secure login with email and password.
* **Password Management**: Add, update, delete, and view passwords for different websites.
* **Password Generation**: Generate secure passwords with one click.
* **Good UI**: Simplistic UI.

## Technologies Used

* **HTML/CSS**: Structure and style the user interface.
* **JavaScript**: Handle form validation, interactivity, and AJAX requests.
* **Flask (Python)**: Backend server to manage user authentication, password data storage, and password management functionality.
* **jQuery**: For handling DOM manipulations (though not strictly necessary, it could be used in the backend to simplify certain tasks).

## Setup Instructions

### Prerequisites

Ensure you have the following installed:

* **Python 3.x** (Install from [python.org](https://www.python.org/downloads/))
* **Flask**: The backend server framework. Install it with:

  ```bash
  pip install flask
  ```


### File Structure

```plaintext
├── templates/
│   ├── index.html          # Index pages (Password Management Page)
│   ├── login.html          # Login page (for user login)
│   └── signup.html         # Sign-up page (for user registration)
└──  app.py                  # Flask backend for handling logic (not included, needs to be created)
```

### Usage

#### 1. **Sign-Up Page (`signup.html`)**

* Navigate to the sign-up page via `http://127.0.0.1:5000/signup`.
* Enter your details:

  * **Name**: Your full name.
  * **Email**: A valid email address.
  * **Password**: A password with at least 8 characters, including one lowercase letter, one uppercase letter, one number, and one special character.
  * **Confirm Password**: Re-enter your password to confirm.

  After validation, the data is sent to the backend to create an account.

#### 2. **Login Page (`login.html`)**

* After registering, you can log in via the `http://127.0.0.1:5000/login`.
* Enter your registered email and password to authenticate.

#### 3. **Password Management Page (`index.html`)**

* Once logged in, you can manage your passwords:

  * **Add Password**: Save a new password for a website.
  * **View Passwords**: See stored passwords (with a toggle to show/hide them).
  * **Update/Delete Password**: Modify or remove stored passwords.
  * **Generate Random Password**: Create secure, random passwords for new accounts.

### Backend API Routes (Flask)

The backend should support the following routes:

1. **`/signup`**: Handles POST requests to register a new user.
2. **`/login`**: Handles POST requests to authenticate a user.
3. **`/logout`**: Logs the user out and ends the session.
4. **`/get_passwords`**: Retrieves all passwords for the logged-in user.
5. **`/save_password`**: Adds a new password entry.
6. **`/update_password/{id}`**: Updates an existing password.
7. **`/delete_password/{id}`**: Deletes a stored password.
8. **`/generate_password`**: Generates a secure random password.

