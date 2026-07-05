import sqlite3
from config import DATABASE_NAME

# =========================
# CONNEXION DB
# =========================
def connect():
    return sqlite3.connect(DATABASE_NAME)

# =========================
# OBTENIR SOLDE
# =========================
def get_balance(nexampay_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT balance FROM users WHERE nexampay_id=?
    """, (nexampay_id,))

    result = cursor.fetchone()
    conn.close()

    if result:
        return result[0]
    return 0

# =========================
# AJOUTER ARGENT (DEPOT)
# =========================
def add_money(nexampay_id, amount):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users SET balance = balance + ?
        WHERE nexampay_id=?
    """, (amount, nexampay_id))

    conn.commit()
    conn.close()

# =========================
# RETIRER ARGENT
# =========================
def withdraw_money(nexampay_id, amount):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT balance FROM users WHERE nexampay_id=?
    """, (nexampay_id,))

    result = cursor.fetchone()

    if result and result[0] >= amount:
        cursor.execute("""
            UPDATE users SET balance = balance - ?
            WHERE nexampay_id=?
        """, (amount, nexampay_id))

        conn.commit()
        conn.close()
        return True

    conn.close()
    return False

# =========================
# TRANSFERT ENTRE UTILISATEURS
# =========================
def transfer_money(sender_id, receiver_id, amount):
    conn = connect()
    cursor = conn.cursor()

    # vérifier solde sender
    cursor.execute("""
        SELECT balance FROM users WHERE nexampay_id=?
    """, (sender_id,))

    sender = cursor.fetchone()

    if not sender or sender[0] < amount:
        conn.close()
        return False

    # débiter sender
    cursor.execute("""
        UPDATE users SET balance = balance - ?
        WHERE nexampay_id=?
    """, (amount, sender_id))

    # créditer receiver
    cursor.execute("""
        UPDATE users SET balance = balance + ?
        WHERE nexampay_id=?
    """, (amount, receiver_id))

    conn.commit()
    conn.close()
    return True