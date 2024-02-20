import sqlite3

# Connect to SQLite database (it will create the file if it does not exist)
conn = sqlite3.connect('chatbot.sqlite')

# Create a cursor object using the cursor() method
cursor = conn.cursor()

# Create table - Users
cursor.execute('''CREATE TABLE IF NOT EXISTS Users
               (user_id TEXT PRIMARY KEY, 
                username TEXT, 
                name TEXT, 
                quota INTEGER)''')

# Create table - Transactions
cursor.execute('''CREATE TABLE IF NOT EXISTS Transactions
               (transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                amount REAL,
                quota_added TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES Users (user_id))''')

# Create table - Transactions
cursor.execute('''CREATE TABLE IF NOT EXISTS Chats
               (chat_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                role TEXT,
                chat TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES Users (user_id))''')

# Commit your changes in the database
conn.commit()

# Close the connection
conn.close()

