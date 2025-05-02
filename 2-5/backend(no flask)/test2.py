import sqlite3

# Connect to the SQLite database (use your database file here)
conn = sqlite3.connect('users.db')

# Create a cursor object to interact with the database
cursor = conn.cursor()

"""
CREATE TABLE IF NOT EXISTS passwords (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        website TEXT NOT NULL,
                        email TEXT NOT NULL,
                        password TEXT NOT NULL,
                        user_email TEXT,
                        FOREIGN KEY (user_email) REFERENCES users(user_email))


"""


# Execute a query to fetch all data from the users table
cursor.execute("SELECT * FROM users")

# Fetch all rows from the executed query
rows = cursor.fetchall()

# Print the rows
print("User Data from the 'users' table:")
for row in rows:
    print(row)

# Close the cursor and connection
cursor.close()
conn.close()


conn = sqlite3.connect('passwords.db')

# Create a cursor object to interact with the database
cursor = conn.cursor()

"""
CREATE TABLE IF NOT EXISTS passwords (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        website TEXT NOT NULL,
                        email TEXT NOT NULL,
                        password TEXT NOT NULL,
                        user_email TEXT,
                        FOREIGN KEY (user_email) REFERENCES users(user_email))


"""


# Execute a query to fetch all data from the users table
user_email=input("enter user_email: ")
cursor.execute("SELECT website,email,password  FROM passwords WHERE user_email = ?", (user_email,))

# Fetch all rows from the executed query
rows = cursor.fetchall()

# Print the rows
print("User Data from the 'users' table:")
for row in rows:
    print(row)

# Close the cursor and connection
cursor.close()
conn.close()
