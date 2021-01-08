#!/usr/bin/python3.7
import logging
import os
import sys
import tempfile
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import engine


def get_telegram_token():
    with open('token.txt', 'r') as f:
        return f.readline().strip()


def on_start(update, context):
    logging.info('Start: ' + str(update))
    msg = "Hello! I'm @FaceDeleteBot. \n Send me photo and I detect and blur all faces on it."
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)


def on_photo(update, context):
    logging.info('Photo: ' + str(update))
    message = update.effective_message
    photos = list(message.photo)
    if message.document:
        photos.append(message.document)

    for p in photos:
        file = context.bot.getFile(p.file_id)
        path = tempfile.gettempdir() + '/' + p.file_id
        logging.info('Input image: ' + path)
        file.download(path)

        output_path = engine.process_image(path)
        logging.info('Output image: ' + output_path)

        with open(output_path, 'rb') as output_photo:
            context.bot.sendPhoto(chat_id=update.effective_chat.id, photo=output_photo,
                                  reply_to_message_id=message.message_id)


def on_unknown(update, context):
    logging.info('Unknown: ' + str(update))
    msg = "Don't understand! Just send me photo and get result :)"
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg,
                             reply_to_message_id=update.effective_message.message_id)


def get_proxy():
    """
    Get proxy config for current deploy
    """
    # for free PythonAnywhere account
    if os.getenv('PYTHONANYWHERE_DOMAIN'):
        return {'proxy_url': 'http://proxy.server:3128'}

    return {}


logging.basicConfig(filename='facedeletebot.log', level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

updater = Updater(get_telegram_token(), request_kwargs=get_proxy())
updater.dispatcher.add_handler(CommandHandler('start', on_start))
updater.dispatcher.add_handler(MessageHandler((Filters.photo | Filters.document) & (~Filters.command), on_photo))
updater.dispatcher.add_handler(MessageHandler(Filters.all, on_unknown))

updater.start_polling()
updater.idle()
