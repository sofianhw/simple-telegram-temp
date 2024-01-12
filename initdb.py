import sqlite3

# Connect to SQLite database (it will create the file if it does not exist)
conn = sqlite3.connect('chatbot.db')

# Create a cursor object using the cursor() method
cursor = conn.cursor()

# Create table - Users
cursor.execute('''CREATE TABLE IF NOT EXISTS Users
               (user_id INTEGER PRIMARY KEY, 
                username TEXT, 
                name TEXT, 
                quota INTEGER)''')

# Create table - Transactions
cursor.execute('''CREATE TABLE IF NOT EXISTS Transactions
               (transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                amount REAL,
                quota_added INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES Users (user_id))''')

# Commit your changes in the database
conn.commit()

# Close the connection
conn.close()

