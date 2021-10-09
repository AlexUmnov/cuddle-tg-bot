import logging
import os

from telegram import update
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram.ext import CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from .scenario_parser import parse_scenarios

PORT = int(os.environ.get('PORT', 8443))
APPLICATION_NAME = f'https://{os.environ.get("HEROKU_APP_NAME", "powerful-everglades-39634")}.herokuapp.com/'
TG_ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
SCENARIOS = parse_scenarios()

def build_keyboard():
    keboard = []
    for key in SCENARIOS['menu']:
        keboard.append(
            InlineKeyboardButton(SCENARIOS[key]['description'], key)
        )
    return InlineKeyboardMarkup(keboard)

def make_response_function(text):
    def response_function(update, context):
        update.message.reply_text(text)
        main_menu(update, None)
    return response_function


def start(bot, update):
    bot.message.reply_text(parse_scenarios["start"])
    main_menu(update, None)

def main_menu(update, context):
    update.message.reply_text("Что тебя интересует?", reply_markup=build_keyboard())

    
def not_command(update, context) -> None:
    update.message.reply_text("Я пока не умею отвечать на сообщения 😔\n Пожалуйста выбери пункт из меню.")

updater = Updater(token=TG_ACCESS_TOKEN, use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

not_command_handler = MessageHandler(Filters.text & (~Filters.command), not_command)
dispatcher.add_handler(not_command_handler)

for key in SCENARIOS:
    updater.dispatcher.add_handler(CallbackQueryHandler(
        make_response_function("\n".join(SCENARIOS[key]["answer"])),
        pattern=key)
    )


updater.start_webhook(listen="0.0.0.0",
                      port=PORT,
                      url_path=TG_ACCESS_TOKEN,
                      webhook_url=APPLICATION_NAME + TG_ACCESS_TOKEN)
updater.idle()