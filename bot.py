#!/usr/bin/python3.7
import logging.config
import os
import sys
import tempfile
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import engine

logger_config = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s: %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'msg': {
            'format': '[%(asctime)s] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'stream': sys.stdout,
        },
        'file_common': {
            'class': 'logging.FileHandler',
            'filename': 'facedeletebot.log',
            'encoding': 'utf-8',
            'formatter': 'default',
        },
        'file_msg': {
            'class': 'logging.FileHandler',
            'filename': 'facedeletebot_msg.log',
            'encoding': 'utf-8',
            'formatter': 'msg',
        },
    },
    'root': {
        'handlers': ['console', 'file_common'],
        'level': 'INFO',
    },
    'loggers': {
        'msg': {
            'handlers': ['console', 'file_msg'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

logging.config.dictConfig(logger_config)
logger_messages = logging.getLogger('msg')


def get_proxy():
    """
    Get proxy config for the current deployment service
    """
    # for free PythonAnywhere account
    if os.getenv('PYTHONANYWHERE_DOMAIN'):
        return {'proxy_url': 'http://proxy.server:3128'}

    return {}


def get_telegram_token():
    with open('token.txt', 'r') as f:
        return f.readline().strip()


def on_start(update, context):
    """Handler for start command"""
    logger_messages.info('Start: ' + str(update))
    msg = "Hello! I'm @FaceDeleteBot. \n Send me photo and I detect and blur all faces on it."
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)


def on_photo(update, context):
    """Handler for photos"""
    logger_messages.info('Photo: ' + str(update))
    message = update.effective_message
    photos = []
    if message.photo:
        photos.append(message.photo[-1])
    if message.document:
        photos.append(message.document)

    for p in photos:
        file = context.bot.getFile(p.file_id)
        path = tempfile.gettempdir() + '/' + p.file_id
        logger_messages.info('Input image: ' + path)
        file.download(path)

        output_path = engine.process_image(path)
        logger_messages.info('Output image: ' + output_path)

        with open(output_path, 'rb') as output_photo:
            context.bot.sendPhoto(chat_id=update.effective_chat.id, photo=output_photo,
                                  reply_to_message_id=message.message_id)


def on_unknown(update, context):
    """Handler for other messages (reply with error)"""
    logger_messages.info('Unknown: ' + str(update))
    msg = "Don't understand! Just send me photo and get result :)"
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg,
                             reply_to_message_id=update.effective_message.message_id)


if __name__ == '__main__':
    updater = Updater(get_telegram_token(), request_kwargs=get_proxy())
    updater.dispatcher.add_handler(CommandHandler('start', on_start))
    updater.dispatcher.add_handler(MessageHandler((Filters.photo | Filters.document) & (~Filters.command), on_photo))
    updater.dispatcher.add_handler(MessageHandler(Filters.all, on_unknown))

    updater.start_polling()
    updater.idle()
