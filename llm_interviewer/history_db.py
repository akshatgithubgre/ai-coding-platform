import sqlite3

DB_NAME = "history.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT,
            answer TEXT,
            correct BOOLEAN,
            difficulty TEXT
        )
    ''')
    conn.commit()
    conn.close()

def store_history(question, answer, correct, difficulty):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO history (question, answer, correct, difficulty)
        VALUES (?, ?, ?, ?)
    ''', (question, answer, correct, difficulty))
    conn.commit()
    conn.close()

def get_history():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT question, answer, correct, difficulty FROM history')
    rows = c.fetchall()
    conn.close()
    return rows
