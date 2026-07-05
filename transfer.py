import sqlite3
from wallet import get_balance
from config import DATABASE_NAME

# =========================
# CONNEXION DB
# =========================
def connect():
    return sqlite3.connect(DATABASE_NAME)

# =========================
# TRANSFERT D'ARGENT
# =========================
def transfer(sender_id, receiver_id, amount):

    conn = connect()
    cursor = conn.cursor()

    # vérifier solde sender
    cursor.execute("""
        SELECT balance FROM users WHERE nexampay_id=?
    """, (sender_id,))

    sender = cursor.fetchone()

    if not sender:
        conn.close()
        return "SENDER_NOT_FOUND"

    if sender[0] < amount:
        conn.close()
        return "INSUFFICIENT_FUNDS"

    # vérifier receiver
    cursor.execute("""
        SELECT balance FROM users WHERE nexampay_id=?
    """, (receiver_id,))

    receiver = cursor.fetchone()

    if not receiver:
        conn.close()
        return "RECEIVER_NOT_FOUND"

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

    # enregistrer transaction sender
    cursor.execute("""
        INSERT INTO transactions (nexampay_id, type, amount, status, description)
        VALUES (?, ?, ?, ?, ?)
    """, (
        sender_id,
        "TRANSFER_OUT",
        amount,
        "SUCCESS",
        f"To {receiver_id}"
    ))

    # enregistrer transaction receiver
    cursor.execute("""
        INSERT INTO transactions (nexampay_id, type, amount, status, description)
        VALUES (?, ?, ?, ?, ?)
    """, (
        receiver_id,
        "TRANSFER_IN",
        amount,
        "SUCCESS",
        f"From {sender_id}"
    ))

    conn.commit()
    conn.close()

    return "SUCCESS"