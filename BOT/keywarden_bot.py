from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from dotenv import load_dotenv
import os
# from ..authentication import login as LG

# accessing the token
load_dotenv()
TOKEN = os.getenv("TOKEN")

# setting up the bot
updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher

# get update from telegram bot: KeyWarden 
updater.start_polling()

# bot functions
def start(update, context):
    update.message.reply_text('Hello welcome to the login/signUp interface of KeyWarden: wielding security for your keys')
dispatcher.add_handler(CommandHandler("start", start))

def login(update, context):
    prev_reply = update.message.text
    update.message.reply_text('LoginID')
    UID = None
    while True:
        print(f"{prev_reply} -> {update.message.text}")
        new_reply = update.message.text
        if str(prev_reply) != str(new_reply):
            UID = update.message.text
            break
    print(UID)
    # context.bot.send_message(update.message.chat_id, 'Please enter your Password')
dispatcher.add_handler(CommandHandler("login", login))



# continuously runs, unless interrupted and listens for updates
updater.idle()
