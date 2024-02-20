import sqlite3, os

def get_db_connection(db_path):
    return sqlite3.connect(f"{db_path}/chatbot.sqlite")

def record_transaction(user_id, amount, quota_added, db_path):
    conn = get_db_connection(db_path)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO Transactions (user_id, amount, quota_added) VALUES (?, ?, ?)", 
                   (user_id, amount, quota_added))
    conn.commit()
    conn.close()

def deposit(user_id, quota, db_path):
    conn = get_db_connection(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT quota FROM Users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()
    quota = user[0] + quota

    cursor.execute("UPDATE Users SET quota = ? WHERE user_id = ?", (quota, user_id))
    conn.commit()
    conn.close()
