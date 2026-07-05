import sqlite3
from wallet import get_balance, withdraw_money
from config import DATABASE_NAME

# =========================
# CONNEXION DB
# =========================
def connect():
    return sqlite3.connect(DATABASE_NAME)

# =========================
# SERVICES TELEGRAM UNIQUES
# =========================
SERVICES = {
    "TELEGRAM_PREMIUM": {
        "name": "Telegram Premium",
        "price": 5000
    },
    "TELEGRAM_STARS": {
        "name": "Telegram Stars",
        "price": 1000
    }
}

# =========================
# ACHETER UN SERVICE
# =========================
def buy_service(nexampay_id, service_key):

    if service_key not in SERVICES:
        return "SERVICE_NOT_FOUND"

    service = SERVICES[service_key]
    price = service["price"]

    balance = get_balance(nexampay_id)

    if balance < price:
        return "INSUFFICIENT_FUNDS"

    # débiter utilisateur
    withdraw_money(nexampay_id, price)

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO transactions (nexampay_id, type, amount, status, description)
        VALUES (?, ?, ?, ?, ?)
    """, (
        nexampay_id,
        "PURCHASE",
        price,
        "SUCCESS",
        service["name"]
    ))

    conn.commit()
    conn.close()

    return "SUCCESS"

# =========================
# LISTE DES SERVICES
# =========================
def get_services():
    return SERVICES