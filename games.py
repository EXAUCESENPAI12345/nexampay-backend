import sqlite3
import random
import time
from wallet import add_money
from config import DATABASE_NAME

# =========================
# CONNEXION DB
# =========================
def connect():
    return sqlite3.connect(DATABASE_NAME)

# =========================
# 🎡 LUCKY SPIN
# =========================
def lucky_spin(nexampay_id):

    rewards = [0, 100, 200, 500, 1000]

    win = random.choice(rewards)

    add_money(nexampay_id, win)

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO transactions (nexampay_id, type, amount, status, description)
        VALUES (?, ?, ?, ?, ?)
    """, (
        nexampay_id,
        "GAME_SPIN",
        win,
        "SUCCESS",
        "Lucky Spin Reward"
    ))

    conn.commit()
    conn.close()

    return win

# =========================
# 🎁 BONUS QUOTIDIEN
# =========================
def daily_bonus(nexampay_id):

    conn = connect()
    cursor = conn.cursor()

    # vérifier dernier bonus
    cursor.execute("""
        SELECT created_at FROM transactions
        WHERE nexampay_id=? AND type='DAILY_BONUS'
        ORDER BY id DESC LIMIT 1
    """, (nexampay_id,))

    last = cursor.fetchone()

    if last:
        return "ALREADY_CLAIMED"

    bonus = random.randint(50, 300)

    add_money(nexampay_id, bonus)

    cursor.execute("""
        INSERT INTO transactions (nexampay_id, type, amount, status, description)
        VALUES (?, ?, ?, ?, ?)
    """, (
        nexampay_id,
        "DAILY_BONUS",
        bonus,
        "SUCCESS",
        "Daily Bonus"
    ))

    conn.commit()
    conn.close()

    return bonus

# =========================
# 🎯 MINI CHALLENGE
# =========================
def mini_challenge(nexampay_id):

    success = random.choice([True, False])

    if success:
        reward = random.randint(100, 500)
        add_money(nexampay_id, reward)

        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO transactions (nexampay_id, type, amount, status, description)
            VALUES (?, ?, ?, ?, ?)
        """, (
            nexampay_id,
            "GAME_CHALLENGE",
            reward,
            "SUCCESS",
            "Challenge Win"
        ))

        conn.commit()
        conn.close()

        return reward

    return 0