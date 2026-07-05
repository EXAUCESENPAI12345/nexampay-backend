import os
import sqlite3

DATABASE_NAME = "/tmp/nexampay.db" if os.getenv("RENDER") else "nexampay.db"

def connect_db():
    return sqlite3.connect(DATABASE_NAME)
def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    # Table utilisateurs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER UNIQUE,
        nexampay_id TEXT UNIQUE,
        username TEXT,
        full_name TEXT,
        phone TEXT,
        password TEXT,
        pin TEXT,
        balance REAL DEFAULT 0,
        is_admin INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Table historique des transactions
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nexampay_id TEXT,
        type TEXT,
        amount REAL,
        status TEXT,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
    print("✅ Base de données NexamPay créée avec succès.")
