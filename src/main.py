import os
from flask import Flask, request
import telebot
import time
from helper.log import log
from helper.api import trending

app = Flask(__name__)
bot = telebot.TeleBot(os.getenv('bot_token'), threaded=False)
previous_message_ids = []

# Bot route to handle incoming messages
@app.route('/bot', methods=['POST'])
def telegram():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return 'OK', 200

# Handler for the '/start' command
@bot.message_handler(commands=['start'])
def start_command(message):
    response_text = "Hello! Welcome to this bot!\n\n"
    response_text += "For help, use the command /help."
    bot.reply_to(message, response_text)

# Handler for the '/help' command
@bot.message_handler(commands=['help'])
def help_command(message):
    response_text = "Here are the available commands:\n\n"
    response_text += "/start - Start the bot.\n"
    response_text += "/help - Show this help message.\n"
    response_text += "/trending - View latest movies.\n"
    bot.reply_to(message, response_text)

@bot.message_handler(commands=['trending'])
def handle_trending(message):
    if message.message_id in previous_message_ids:
         return
    previous_message_ids.append(message.message_id)

    full_list = trending(1)
    print(full_list)
    for movie in full_list:
        caption = f"{movie['title']} ({movie['year']})\n {movie['rating']} ⭐ \n{movie['url']}"
        image = movie['image']
        bot.send_photo(message.chat.id, image, caption = caption)
    bot.send_message(message.chat.id, '/trending2')

# Handler for any other message
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    bot.reply_to(message, message.text)

