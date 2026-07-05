import requests
from config import DATABASE_NAME

# =========================
# CONFIG MOBILE FUSION
# =========================
API_URL = "https://api.mobilefusion.com/v1"
API_KEY = "YOUR_API_KEY"
API_SECRET = "YOUR_API_SECRET"

# =========================
# CONNEXION API
# =========================
def headers():
    return {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

# =========================
# 💰 DEPOT MOBILE MONEY
# =========================
def send_deposit(phone, amount, operator):

    payload = {
        "phone": phone,
        "amount": amount,
        "operator": operator,
        "type": "deposit"
    }

    try:
        response = requests.post(
            f"{API_URL}/deposit",
            json=payload,
            headers=headers()
        )

        return response.json()

    except Exception as e:
        return {"status": "error", "message": str(e)}

# =========================
# 🏧 RETRAIT MOBILE MONEY
# =========================
def send_withdrawal(phone, amount, operator):

    payload = {
        "phone": phone,
        "amount": amount,
        "operator": operator,
        "type": "withdrawal"
    }

    try:
        response = requests.post(
            f"{API_URL}/withdraw",
            json=payload,
            headers=headers()
        )

        return response.json()

    except Exception as e:
        return {"status": "error", "message": str(e)}

# =========================
# 📊 VERIFIER TRANSACTION
# =========================
def check_transaction(transaction_id):

    try:
        response = requests.get(
            f"{API_URL}/transaction/{transaction_id}",
            headers=headers()
        )

        return response.json()

    except Exception as e:
        return {"status": "error", "message": str(e)}