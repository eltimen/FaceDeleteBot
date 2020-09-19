#!/usr/bin/python3.7
import telepot
import time
import urllib3
import urllib3.request
import tempfile
import logging
import sys

import engine


def get_telegram_token():
    with open('token.txt', 'r') as f:
        return f.readline().strip()


def download_image(msg):
    if len(msg['photo']) == 0:
        return ''

    file_name = msg['photo'][-1]['file_id']
    path = tempfile.gettempdir() + '/' + file_name
    bot.download_file(file_name, path)
    return path


def handle(msg):
    logging.info(msg)
    content_type, chat_type, chat_id = telepot.glance(msg)

    if content_type == 'text' and msg['text'] == '/start':
        bot.sendMessage(chat_id, "Hello! I'm @FaceDeleteBot. \n Send me photo and I detect and blur all faces on it.")
    elif content_type == 'photo':
        path = download_image(msg)
        output_path = engine.process_image(path)
        logging.info('Input image: ' + path)
        logging.info('Output image: ' + output_path)
        with open(output_path, 'rb') as output_photo:
            bot.sendPhoto(chat_id, output_photo, reply_to_message_id=msg['message_id'])
    else:
        bot.sendMessage(chat_id, "Don't understand! Just send me photo and get result :)",
                        reply_to_message_id=msg['message_id'])


def setup_pyanywhere_free_proxy():
    """
    Setup proxy for free PythonAnywhere account
    """
    proxy_url = "http://proxy.server:3128"
    telepot.api._pools = {
        'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
    }
    telepot.api._onetime_pool_spec = (
        urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30)
    )


setup_pyanywhere_free_proxy()
logging.basicConfig(filename='facedeletebot.log', level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
bot = telepot.Bot(get_telegram_token())
bot.message_loop(handle)
print('Listening ...')

while 1:
    time.sleep(10)
