import sqlite3
from wallet import get_balance, withdraw_money
from config import DATABASE_NAME

# =========================
# CONNEXION DB
# =========================
def connect():
    return sqlite3.connect(DATABASE_NAME)

# =========================
# PAIEMENT TELEGRAM UNIQUEMENT
# =========================
def make_payment(nexampay_id, amount, service_name):

    # services autorisés
    allowed_services = [
        "TELEGRAM_PREMIUM",
        "TELEGRAM_STARS"
    ]

    if service_name not in allowed_services:
        return "SERVICE_NOT_ALLOWED"

    conn = connect()
    cursor = conn.cursor()

    # vérifier solde
    balance = get_balance(nexampay_id)

    if balance < amount:
        conn.close()
        return "INSUFFICIENT_FUNDS"

    # débiter wallet
    withdraw_money(nexampay_id, amount)

    # enregistrer transaction
    cursor.execute("""
        INSERT INTO transactions (nexampay_id, type, amount, status, description)
        VALUES (?, ?, ?, ?, ?)
    """, (
        nexampay_id,
        "PAYMENT",
        amount,
        "SUCCESS",
        service_name
    ))

    conn.commit()
    conn.close()

    return "SUCCESS"