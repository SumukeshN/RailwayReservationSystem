import sqlite3

def login_user(username, password):
    conn = sqlite3.connect('railway.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    result = cursor.fetchone()

    conn.close()
    return result is not None
