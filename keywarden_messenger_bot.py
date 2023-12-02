import telebot
from telebot import types
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("KEYWARDEN_MESSENGER_TOKEN")

# create the bot
bot = telebot.TeleBot(TOKEN)

def send_OTP(target_chat_id, OTP):
    bot.send_message(target_chat_id, OTP)

if __name__ == "__main__":
    bot.polling()
    send_OTP("khritish17", "789")