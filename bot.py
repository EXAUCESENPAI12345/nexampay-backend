from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

from auth import create_user, get_user

TOKEN = "8116900179:AAE9oupmb8i_eEyDCQR4-ta3eZ9frab4kkI"
MINI_APP_URL = "https://nexampay.netlify.app"

# =========================
# /start
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    create_user(user.id, user.username, user.full_name)

    keyboard = [
        [
            InlineKeyboardButton(
                "🚀 Ouvrir NexamPay",
                web_app=WebAppInfo(url=MINI_APP_URL)
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "👋 Bienvenue sur NexamPay\n\nClique pour ouvrir l'application :",
        reply_markup=reply_markup
    )

# =========================
# MAIN
# =========================
def main():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    print("Bot NexamPay démarré...")

    app.run_polling()

if __name__ == "__main__":
    main()