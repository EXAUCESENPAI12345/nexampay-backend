import sqlite3
from config import DATABASE_NAME

# =========================
# CONNEXION DB
# =========================
def connect():
    return sqlite3.connect(DATABASE_NAME)

# =========================
# 📊 STATS GLOBALES
# =========================
def get_stats():

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM users")
    users = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(amount) FROM transactions WHERE status='SUCCESS'")
    total_money = cursor.fetchone()[0] or 0

    cursor.execute("SELECT COUNT(*) FROM transactions")
    transactions = cursor.fetchone()[0]

    conn.close()

    return {
        "users": users,
        "total_money": total_money,
        "transactions": transactions
    }

# =========================
# 👥 LISTER UTILISATEURS
# =========================
def get_all_users():

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT nexampay_id, username, balance, created_at
        FROM users
    """)

    data = cursor.fetchall()
    conn.close()

    return data

# =========================
# 💰 MODIFIER SOLDE USER
# =========================
def set_balance(nexampay_id, amount):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users SET balance=?
        WHERE nexampay_id=?
    """, (amount, nexampay_id))

    conn.commit()
    conn.close()

    return True

# =========================
# 🚨 BANNIR / DEBANNIR USER
# =========================
def delete_user(nexampay_id):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM users WHERE nexampay_id=?
    """, (nexampay_id,))

    conn.commit()
    conn.close()

    return True