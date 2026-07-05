import sqlite3
import time
from wallet import add_money
from config import DATABASE_NAME

# =========================
# CONNEXION DB
# =========================
def connect():
    return sqlite3.connect(DATABASE_NAME)

# =========================
# CREER UNE DEMANDE DE DEPOT
# =========================
def create_deposit(nexampay_id, amount, phone, operator):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO transactions (nexampay_id, type, amount, status, description)
        VALUES (?, ?, ?, ?, ?)
    """, (
        nexampay_id,
        "DEPOSIT",
        amount,
        "PENDING",
        f"{operator} | {phone}"
    ))

    conn.commit()
    conn.close()

    return True

# =========================
# CONFIRMER DEPOT (APRES MOBILE FUSION)
# =========================
def confirm_deposit(transaction_id, nexampay_id, amount):
    conn = connect()
    cursor = conn.cursor()

    # mettre statut success
    cursor.execute("""
        UPDATE transactions
        SET status='SUCCESS'
        WHERE id=?
    """, (transaction_id,))

    conn.commit()
    conn.close()

    # créditer le wallet
    add_money(nexampay_id, amount)

    return True

# =========================
# ECHEC DE DEPOT
# =========================
def fail_deposit(transaction_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE transactions
        SET status='FAILED'
        WHERE id=?
    """, (transaction_id,))

    conn.commit()
    conn.close()

    return True