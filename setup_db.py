import sqlite3

def setup_db():
    conn = sqlite3.connect("budget.db")
    cursor = conn.cursor()

    # Drop tables if they exist
    cursor.execute("DROP TABLE IF EXISTS income")
    cursor.execute("DROP TABLE IF EXISTS expenses")
    cursor.execute("DROP TABLE IF EXISTS savings")

    # Create tables
    cursor.execute('''CREATE TABLE IF NOT EXISTS income (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        amount REAL,
                        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        category TEXT,
                        amount REAL,
                        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS savings (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        goal REAL,
                        contribution REAL DEFAULT 0,
                        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )''')

    conn.commit()
    conn.close()

setup_db()
