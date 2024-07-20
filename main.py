from flask import Flask
from threading import Thread
from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackContext
from telegram import Update
import os
import schedule
import time

app = Flask(__name__)

@app.route('/')
def index():
    return "Bot is running"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

async def respond_to_user(update: Update, context: CallbackContext) -> None:
    TARGET_USER_ID = 6812654722
    user_states = {}

    if update.message.from_user.id == TARGET_USER_ID:
        user_id = update.message.from_user.id

        if user_id in user_states and user_states[user_id] == 'answered':
            return

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

def main() -> None:
    TOKEN = os.getenv('TOKEN', 'YOUR_TOKEN')
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), respond_to_user))

    schedule.every().day.at("00:00").do(lambda: user_states.clear())
    while True:
        schedule.run_pending()
        time.sleep(1)

    application.run_polling()

if __name__ == '__main__':
    Thread(target=run_flask).start()
    main()
