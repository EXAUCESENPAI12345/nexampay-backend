import sqlite3
from wallet import withdraw_money
from config import DATABASE_NAME

# =========================
# CONNEXION DB
# =========================
def connect():
    return sqlite3.connect(DATABASE_NAME)

# =========================
# DEMANDE DE RETRAIT
# =========================
def create_withdrawal(nexampay_id, amount, phone, operator):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO transactions (nexampay_id, type, amount, status, description)
        VALUES (?, ?, ?, ?, ?)
    """, (
        nexampay_id,
        "WITHDRAWAL",
        amount,
        "PENDING",
        f"{operator} | {phone}"
    ))

    conn.commit()
    conn.close()

    return "PENDING"

# =========================
# CONFIRMER RETRAIT (Mobile Fusion OK)
# =========================
def confirm_withdrawal(transaction_id, nexampay_id, amount):

    conn = connect()
    cursor = conn.cursor()

    # retirer argent du wallet
    success = withdraw_money(nexampay_id, amount)

    if not success:
        conn.close()
        return "FAILED_INSUFFICIENT_FUNDS"

    # mettre statut success
    cursor.execute("""
        UPDATE transactions
        SET status='SUCCESS'
        WHERE id=?
    """, (transaction_id,))

    conn.commit()
    conn.close()

    return "SUCCESS"

# =========================
# ECHEC RETRAIT
# =========================
def fail_withdrawal(transaction_id):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE transactions
        SET status='FAILED'
        WHERE id=?
    """, (transaction_id,))

    conn.commit()
    conn.close()

    return "FAILED"