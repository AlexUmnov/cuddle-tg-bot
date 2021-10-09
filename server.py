import logging
import os
from telegram import update

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters

PORT = int(os.environ.get('PORT', 8443))
APPLICATION_NAME = f'https://{os.environ.get("HEROKU_APP_NAME", "powerful-everglades-39634")}.herokuapp.com/'
TG_ACCESS_TOKEN = os.environ['ACCESS_TOKEN']

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"You said {update.message.text}")

updater = Updater(token=TG_ACCESS_TOKEN, use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)


updater.start_webhook(listen="0.0.0.0",
                      port=PORT,
                      url_path=TG_ACCESS_TOKEN,
                      webhook_url=APPLICATION_NAME + TG_ACCESS_TOKEN)
updater.idle()