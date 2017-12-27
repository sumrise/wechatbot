#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2017/12/12 上午11:07
# @Author  : guowei
# @Site    : 
# @File    : tgbot.py
# @Software: PyCharm
import logging
import telegram
from flask import Flask, request

import job
from main import getCoinMsg

TOKEN = '496417543:AAFhOeG4UrsgnZ789nAViDeX6mEsU3RjqEI'
bot_name = 'sumchain_bot'
global bot

pp = telegram.utils.request.Request(proxy_url='http://127.0.0.1:1087')
bot = telegram.Bot(token=TOKEN, request=pp)
app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
bot_name = '@sumchain_bot'

MY_CHAT_ID = 412825197
GROUP_CHAT_ID = -1001204895054


@app.route('/hello')
def hello_world():
    return 'Hello World!'


@app.route('/send')
def send():
    message = request.args.get('message', '')
    type = request.args.get('type', '')
    if type == 'group':
        bot.sendMessage(chat_id=GROUP_CHAT_ID, text=message, timeout=5000)
    else:
        bot.sendMessage(chat_id=MY_CHAT_ID, text=message, timeout=5000)


def send_msg(text):
    bot.sendMessage(chat_id=GROUP_CHAT_ID, text=text, timeout=5000)


@app.route('/')
def start(message):
    bot.sendMessage(chat_id=message.chat_id, text='I\'am a sumbot,please talk to me !', timeout=5000)


@app.route('/launcher', methods=['POST', 'GET'])
def launcher():
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        handle_message(update.message)
    return 'ok'


def handle_message(message):
    text = message.text
    if text is None:
        return
    elif '/A' in text:
        getCoinPrice(message)

    logging.info(text)


def getCoinPrice(message):
    cmd, text = parse_cmd_text(message.text)
    logging.info(text)
    if text is None:
        return
    result = getCoinMsg(text)
    if result == '':
        result = u'未找到'
    bot.sendMessage(chat_id=message.chat_id, text=result, timeout=5000)


def echo(message):
    """
     repeat the same message back (echo)
     """
    cmd, text = parse_cmd_text(message.text)
    if text == None or len(text) == 0:
        pass
    else:
        chat_id = message.chat.id
        bot.sendMessage(chat_id=chat_id, text=text)


def parse_cmd_text(text):
    # Telegram understands UTF-8, so encode text for unicode compatibility
    # text = text.encode('utf-8')
    cmd = None
    if '/' in text:
        try:
            index = text.index(' ')
        except ValueError as e:
            return (text, None)
        cmd = text[:index]
        text = text[index + 1:]
    if not cmd == None and '@' in cmd:
        cmd = cmd.replace(bot_name, '')
    return (cmd, text)


if __name__ == '__main__':
    app.debug = True
    job.job_start()
    app.run(host='0.0.0.0', port=5001)
