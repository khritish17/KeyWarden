import telebot
from telebot import types
from dotenv import load_dotenv
import os
import authentication as auth
import password_manager as PM

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
    login_signup(msg)
# asks user whether to login or signup
def login_signup(message):
    markup = types.InlineKeyboardMarkup()
    login_button = types.InlineKeyboardButton("LOGIN", callback_data = "login")
    signup_button = types.InlineKeyboardButton("SIGNUP", callback_data = "signup")
    markup.add(login_button, signup_button)
    bot.send_message(message.chat.id, "Would you like to:", reply_markup=markup)
# querry handler to decide to proceed with login/signup based on users reply
@bot.callback_query_handler(func=lambda call: True)
def login_signup_decide(call):
    if call.data == "login":
        user_data["query"] = "login"
        msg = bot.send_message(call.message.chat.id, "Please enter your details for the login procedure")
        ask_login_UID(msg)
    elif call.data == "signup":
        user_data["query"] = "signup"
        msg = bot.send_message(call.message.chat.id, "Kindly input your details for the signup procedure")
        ask_signup_UID(msg)
    elif call.data == "append":
        msg = bot.send_message(call.message.chat.id, "Input the following parameter:")
        ask_text(msg)
    elif call.data == "req_all":
        pass
    elif call.data == "history":
        pass

    # bot.delete_message(call.message.chat.id, call.message.message_id)
    # bot.delete_message(call.message.chat.id, call.message.message_id -1 )

# signup interfarce
def ask_signup_UID(message):
    msg = bot.send_message(message.chat.id, "Please supply a unique user ID; it is strongly advised to utilize your Telegram mobile number")
    bot.register_next_step_handler(msg, get_signup_UID)
def get_signup_UID(message):
    user_data['signup_UID'] = message.text
    ask_signup_PWD(message)
def ask_signup_PWD(message):
    msg = bot.send_message(message.chat.id, "Please enter a password, ensuring to commit it to memory as recovery is not possible")
    bot.register_next_step_handler(msg, get_signup_PWD)
def get_signup_PWD(message):
    user_data["signup_PWD"] = message.text
    authenticate_signup(message)
def authenticate_signup(message):
    signup_UID = user_data["signup_UID"]
    signup_PWD = user_data["signup_PWD"]
    signup_chat_id = message.chat.id
    if auth.signup(signup_UID, signup_PWD, signup_chat_id):
        bot.send_message(message.chat.id, "Signup successfull!")
        ask_login_UID(message)
    else:
        bot.send_message(message.chat.id, "Signup unsuccessfull!")
        bot.send_message(message.chat.id, "Login with the user id and password")
        login_signup(message)

# login interface
def ask_login_UID(message):
    msg = bot.send_message(message.chat.id, "Please provide your login ID")
    bot.register_next_step_handler(msg, get_login_UID)
def get_login_UID(message):
    user_data['login_UID'] = message.text
    ask_login_PWD(message)
def ask_login_PWD(message):
    msg = bot.send_message(message.chat.id, "Kindly input the password")
    bot.register_next_step_handler(msg, get_login_PWD)
def get_login_PWD(message):
    user_data['login_PWD'] = message.text
    bot.delete_message(message.chat.id, message.message_id)
    bot.delete_message(message.chat.id, message.message_id -1)
    bot.delete_message(message.chat.id, message.message_id -2)
    bot.delete_message(message.chat.id, message.message_id -3)
    bot.delete_message(message.chat.id, message.message_id -4)
    authenticate_login(message)
def authenticate_login(message):
    login_UID = user_data["login_UID"]
    login_PWD = user_data["login_PWD"]
    if auth.login(login_UID, login_PWD):
        bot.send_message(message.chat.id, "Login successfull!")
        PWD_manager(message)
    else:
        bot.send_message(message.chat.id, "Login unsuccessfull!")
        login_signup(message)
def PWD_manager(message):
    bot.send_message(message.chat.id,"The following opeartions can be performed:")
    bot.send_message(message.chat.id, "ADD:\tTo add a new login credential")
    bot.send_message(message.chat.id, "REQ_ALL:\tTo get all login credential")
    bot.send_message(message.chat.id, "HISTORY:\tTo get the transaction history")
    markup = types.InlineKeyboardMarkup()
    ADD_button = types.InlineKeyboardButton("ADD", callback_data = "append")
    REQ_ALL_button = types.InlineKeyboardButton("REQ_ALL", callback_data = "req_all")
    HISTORY_button = types.InlineKeyboardButton("HISTORY", callback_data = "history")
    markup.add(ADD_button, REQ_ALL_button, HISTORY_button)
    bot.send_message(message.chat.id, "Choose an operation", reply_markup=markup)


# append interface
append_data = {"append_text":None, "generate":None, "append_UID":None, "append_PWD": "", "append_masterpassword": None}
def ask_text(message):
    msg = bot.send_message(message.chat.id, "Please give a name to the credentials. e.g GitHub or Gmail")
    bot.register_next_step_handler(msg, get_text)
def get_text(message):
    append_data["append_text"] = message.text
    ask_append_UID(message)
def ask_append_UID(message):
    msg= bot.send_message(message.chat.id, f"Provide the LoginID you have used in {append_data['append_text']}")
    bot.register_next_step_handler(msg, get_append_UID)
def get_append_UID(message):
    append_data["append_UID"] = message.text
    ask_to_generate_PWD(message)
def ask_to_generate_PWD(message):
    msg = bot.send_message(message.chat.id, "Would you like to generate a strong password or do you prefer using one of yours\n\nType Y for YES\nType N for NO")
    bot.register_next_step_handler(msg, decide_to_generate_PWD)
def decide_to_generate_PWD(message):
    response = (message.text).lower()
    append_data["generate"] = True if response == 'y' else False
    if not append_data["generate"]:
        ask_append_PWD(message)
    else:
        ask_masterpassword(message)
def ask_append_PWD(message):
    msg = bot.send_message(message.chat.id, "Provide a strong password")
    bot.register_next_step_handler(msg, get_append_PWD)
def get_append_PWD(message):
    append_data["append_PWD"] = message.text
    ask_masterpassword(message)
def ask_masterpassword(message):
    msg = bot.send_message(message.chat.id, "Provide a masterpassword...do not forget this master-password, otherwise your passwords can not be retrived")
    bot.register_next_step_handler(msg, get_masterpassword)
def get_masterpassword(message):
    append_data["append_masterpassword"] = message.text
    append_credential(message)
def append_credential(message):
    append_UID = user_data["login_UID"]
    append_masterPWD = append_data["append_masterpassword"]
    append_loginID = append_data["append_UID"]
    append_PWD = append_data["append_PWD"]
    append_generate = append_data["generate"]
    append_text = append_data["append_text"]
    if PM.append(UID=append_UID, masterpassword=append_masterPWD, loginID=append_loginID, PWD=append_PWD,text= append_text, generate= append_generate):
        msg =bot.send_message(message.chat.id, "Successfully and securely added the Credential")
        PWD_manager(msg)

    

# delete interface
# history


if __name__ == '__main__':
    bot.polling()