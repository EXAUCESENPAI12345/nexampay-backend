import sqlite3
import random
import string
from config import DATABASE_NAME

# =========================
# CONNEXION DB
# =========================
def connect():
    return sqlite3.connect(DATABASE_NAME)

# =========================
# GENERER ID NEXAMPAY
# =========================
def generate_nexampay_id():
    return "NEX" + "".join(random.choices(string.digits, k=6))

# =========================
# CREER UTILISATEUR
# =========================
def create_user(telegram_id, username, full_name):
    conn = connect()
    cursor = conn.cursor()

    nexampay_id = generate_nexampay_id()

    cursor.execute("""
        INSERT OR IGNORE INTO users 
        (telegram_id, nexampay_id, username, full_name)
        VALUES (?, ?, ?, ?)
    """, (telegram_id, nexampay_id, username, full_name))

    conn.commit()
    conn.close()

    return nexampay_id

# =========================
# RECUPERER UTILISATEUR
# =========================
def get_user(telegram_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM users WHERE telegram_id=?
    """, (telegram_id,))

    user = cursor.fetchone()
    conn.close()
    return user

# =========================
# VERIFIER ADMIN
# =========================
def is_admin(telegram_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT is_admin FROM users WHERE telegram_id=?
    """, (telegram_id,))

    result = cursor.fetchone()
    conn.close()

    if result and result[0] == 1:
        return True
    return False