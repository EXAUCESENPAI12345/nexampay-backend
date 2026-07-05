from flask import Flask, request, jsonify

from auth import create_user, get_user
from wallet import get_balance
from deposit import create_deposit
from withdrawal import create_withdrawal
from transfer import transfer
from payment import make_payment
from purchase import buy_service
from games import lucky_spin, daily_bonus, mini_challenge
from mobilefusion import send_deposit, send_withdrawal

app = Flask(__name__)

# =========================
# 👤 CREER UTILISATEUR (TELEGRAM)
# =========================
@app.route("/user/create", methods=["POST"])
def api_create_user():

    data = request.json

    telegram_id = data["telegram_id"]
    username = data["username"]
    full_name = data["full_name"]

    nexampay_id = create_user(telegram_id, username, full_name)

    return jsonify({
        "status": "success",
        "nexampay_id": nexampay_id
    })

# =========================
# 💰 SOLDE
# =========================
@app.route("/wallet/balance", methods=["GET"])
def api_balance():

    nexampay_id = request.args.get("nexampay_id")

    balance = get_balance(nexampay_id)

    return jsonify({
        "balance": balance
    })

# =========================
# 💰 DEPOT
# =========================
@app.route("/deposit", methods=["POST"])
def api_deposit():

    data = request.json

    nexampay_id = data["nexampay_id"]
    amount = data["amount"]
    phone = data["phone"]
    operator = data["operator"]

    # appel Mobile Fusion
    response = send_deposit(phone, amount, operator)

    create_deposit(nexampay_id, amount, phone, operator)

    return jsonify(response)

# =========================
# 🏧 RETRAIT
# =========================
@app.route("/withdraw", methods=["POST"])
def api_withdraw():

    data = request.json

    nexampay_id = data["nexampay_id"]
    amount = data["amount"]
    phone = data["phone"]
    operator = data["operator"]

    response = send_withdrawal(phone, amount, operator)

    create_withdrawal(nexampay_id, amount, phone, operator)

    return jsonify(response)

# =========================
# 🔄 TRANSFERT
# =========================
@app.route("/transfer", methods=["POST"])
def api_transfer():

    data = request.json

    result = transfer(
        data["sender_id"],
        data["receiver_id"],
        data["amount"]
    )

    return jsonify({"status": result})

# =========================
# 💳 PAIEMENT
# =========================
@app.route("/payment", methods=["POST"])
def api_payment():

    data = request.json

    result = make_payment(
        data["nexampay_id"],
        data["amount"],
        data["service_name"]
    )

    return jsonify({"status": result})

# =========================
# 🛒 ACHAT
# =========================
@app.route("/purchase", methods=["POST"])
def api_purchase():

    data = request.json

    result = buy_service(
        data["nexampay_id"],
        data["service_key"]
    )

    return jsonify({"status": result})

# =========================
# 🎮 JEUX
# =========================
@app.route("/games/spin", methods=["POST"])
def api_spin():

    nexampay_id = request.json["nexampay_id"]

    reward = lucky_spin(nexampay_id)

    return jsonify({"reward": reward})

@app.route("/games/daily", methods=["POST"])
def api_daily():

    nexampay_id = request.json["nexampay_id"]

    reward = daily_bonus(nexampay_id)

    return jsonify({"reward": reward})

@app.route("/games/challenge", methods=["POST"])
def api_challenge():

    nexampay_id = request.json["nexampay_id"]

    reward = mini_challenge(nexampay_id)

    return jsonify({"reward": reward})

# =========================
# 🚀 LANCEMENT SERVEUR
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)