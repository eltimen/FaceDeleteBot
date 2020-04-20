#!/usr/bin/python3.7
import telepot
import time
import urllib3
import urllib3.request
import tempfile

import engine

# You can leave this bit out if you're using a paid PythonAnywhere account
proxy_url = "http://proxy.server:3128"
telepot.api._pools = {
    'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
}
telepot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))
# end of the stuff that's only needed for free accounts

def get_telegram_token():
    with open('token.txt', 'r') as f:
        return f.readline().strip()

bot = telepot.Bot(get_telegram_token())

def download_image(msg):
    if len(msg['photo'])==0:
        return ''

    file_name = msg['photo'][-1]['file_id']
    path = tempfile.gettempdir()+'/' + file_name
    bot.download_file(file_name, path)
    print(path)
    return path


def handle(msg):
    print(msg)
    content_type, chat_type, chat_id = telepot.glance(msg)

    if content_type == 'photo':
        path = download_image(msg)
        modified_path = engine.process_image(path)
        with open(modified_path, 'rb') as modified_photo:
            bot.sendPhoto(chat_id, modified_photo, reply_to_message_id=msg['message_id'])
    else:
        bot.sendMessage(chat_id, "Don't understand! Just send me photo and get result :)")

bot.message_loop(handle)

print ('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)