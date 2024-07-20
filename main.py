from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackContext
from telegram import Update
import schedule
import time
import threading

TOKEN = '7473265259:AAFnIVKFpAtxWxdJAKzWaQoM79X5IgAo_cw'  # Remplacez avec votre vrai token
TARGET_USER_ID = 6812654722  # Remplacez avec l'ID utilisateur ciblé

# Dictionnaire pour stocker l'état de la conversation par utilisateur
user_states = {}


async def respond_to_user(update: Update, context: CallbackContext) -> None:
    if update.message.from_user.id == TARGET_USER_ID:
        user_id = update.message.from_user.id

        # Vérifier si l'utilisateur a déjà répondu oui ou non
        if user_id in user_states and user_states[user_id] == 'answered':
            return  # Ne rien faire si l'utilisateur a déjà répondu

        message_text = update.message.text.lower()

        if message_text == "oui":
            await update.message.reply_text("sale cuck ntm")
            user_states[user_id] = 'answered'
        elif message_text == "non":
            await update.message.reply_text("ok go discord + café")
            user_states[user_id] = 'answered'
        else:
            await update.message.reply_text("Bonjour! Veux-tu discuter? (oui/non)")
            user_states[user_id] = 'question_asked'


def reset_user_state():
    global user_states
    user_states = {}
    print("État utilisateur réinitialisé")


def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)


def main() -> None:
    print("Démarrage du bot...")

    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), respond_to_user))

    # Planifier la réinitialisation quotidienne
    schedule.every().day.at("00:00").do(reset_user_state)
    threading.Thread(target=run_schedule, daemon=True).start()

    try:
        application.run_polling()
    except Exception as e:
        print(f"Erreur rencontrée lors de l'exécution du bot : {e}")


if __name__ == '__main__':
    main()
