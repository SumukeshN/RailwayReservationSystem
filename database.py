import sqlite3

def create_tables():
    conn = sqlite3.connect("railway.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS bookings (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, train TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS trains (name TEXT, time TEXT, origin TEXT, destination TEXT)")
    conn.commit()
    conn.close()

def add_train(name, time, origin, destination):
    conn = sqlite3.connect("railway.db")
    c = conn.cursor()
    c.execute("INSERT INTO trains (name, time, origin, destination) VALUES (?, ?, ?, ?)", 
              (name, time, origin, destination))
    conn.commit()
    conn.close()

def get_trains():
    conn = sqlite3.connect("railway.db")
    c = conn.cursor()
    c.execute("SELECT name, time, origin, destination FROM trains")
    rows = c.fetchall()
    conn.close()
    return [{"name": r[0], "time": r[1], "from": r[2], "to": r[3]} for r in rows]

def book_train(username, train_name):
    conn = sqlite3.connect("railway.db")
    c = conn.cursor()
    c.execute("INSERT INTO bookings (username, train) VALUES (?, ?)", (username, train_name))
    conn.commit()
    conn.close()

def get_booking_history(username):
    conn = sqlite3.connect("railway.db")
    c = conn.cursor()
    c.execute("SELECT train FROM bookings WHERE username=?", (username,))
    bookings = [row[0] for row in c.fetchall()]
    conn.close()
    return bookings

def cancel_booking(username, train_name):
    conn = sqlite3.connect("railway.db")
    c = conn.cursor()
    c.execute("DELETE FROM bookings WHERE username=? AND train=? LIMIT 1", (username, train_name))
    conn.commit()
    conn.close()
