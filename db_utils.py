import sqlite3, os

def get_db_connection():
    return sqlite3.connect('chatbot.db')

def register_user(user_id, username, name):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()

    if not user:
        cursor.execute("INSERT INTO Users (user_id, username, name, quota) VALUES (?, ?, ?, ?)", 
                       (user_id, username, name, 10))
        conn.commit()
        response = os.environ.get('NEW_REGISTER')
    else:
        response = "Already registered."

    conn.close()
    return response

def get_user_quota(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT quota FROM Users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()

    conn.close()
    return user[0] if user else None

def decrease_quota(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT quota FROM Users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()

    if user and user[0] > 0:
        new_quota = user[0] - 1
        cursor.execute("UPDATE Users SET quota = ? WHERE user_id = ?", (new_quota, user_id))
        conn.commit()
        conn.close()
        return new_quota
    else:
        conn.close()
        return None

def record_transaction(user_id, amount, quota_added):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO Transactions (user_id, amount, quota_added) VALUES (?, ?, ?)", 
                   (user_id, amount, quota_added))
    conn.commit()
    conn.close()

def deposit(user_id, quota):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT quota FROM Users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()
    quota = user[0] + quota

    cursor.execute("UPDATE Users SET quota = ? WHERE user_id = ?", (quota, user_id))
    conn.commit()
    conn.close()
