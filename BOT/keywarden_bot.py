import telebot
from telebot import types
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("KEYWARDEN_TOKEN")

# create the bot
bot = telebot.TeleBot(TOKEN)
# user_data
user_data = {'query': None, 'login_UID': None, 'login_PWD':None, 'signup_UID': None, 'signup_PWD': None, 'mob_no':None}

# start function
@bot.message_handler(commands=['start'])
def start(message):
    msg = bot.send_message(message.chat.id, "Hi this is KeyWarden Bot!!!")
    # bot.register_next_step_handler(msg, ask_login_signup)
    ask_login_signup(message)

# ask whether for login or signup
def ask_login_signup(message):
    msg = bot.send_message(message.chat.id, "Enter:\n1 to login\n2 to signup")
    bot.register_next_step_handler(msg, get_login_signup)
# get the response for login or signup
def get_login_signup(message):
    user_data['query'] = message.text
    # bot.register_next_step_handler(message, decide_login_signup)
    decide_login_signup(message)

# decide whether login or signup based on given query
# query = 1-> login
# query = 2 -> signup

def decide_login_signup(message):
    if user_data['query'] == "1":
        ask_login_UID(message)
    elif user_data['query'] == "2":
        print("Signup")
    else:
        ask_login_signup(message)

# login interface
def ask_login_UID(message):
    msg = bot.send_message(message.chat.id, "Enter your login ID")
    bot.register_next_step_handler(msg, get_login_UID)
def get_login_UID(message):
    user_data['login_UID'] = message.text
    ask_login_PWD(message)
def ask_login_PWD(message):
    msg = bot.send_message(message.chat.id, "Enter the password")
    bot.register_next_step_handler(msg, get_login_PWD)
def get_login_PWD(message):
    user_data['login_PWD'] = message.text
    print(f"LoginID:{user_data['login_UID']}, PWD:{user_data['login_PWD']}")



if __name__ == '__main__':
    bot.polling()