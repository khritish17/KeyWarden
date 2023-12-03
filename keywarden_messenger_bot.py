import telebot
from telebot import types
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("KEYWARDEN_TOKEN")

# create the bot
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    # Create a dynamic keyboard with buttons based on your data
    keyboard = create_dynamic_keyboard()

    # Send a message with the dynamic keyboard
    bot.send_message(message.chat.id, "Choose an option:", reply_markup=keyboard)

def create_dynamic_keyboard():
    # Simulate dynamic data for the buttons (replace this with your data)
    button_labels = ["Button 1", "Button 2", "Button 3"]

    # Create a ReplyKeyboardMarkup
    # keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard = types.InlineKeyboardMarkup()
    for label in button_labels:
        button = types.InlineKeyboardButton(label, callback_data=label)
        keyboard.add(button)

    return keyboard

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    # Handle other messages if needed
    pass

if __name__ == "__main__":
    bot.polling()
