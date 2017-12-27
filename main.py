#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/11/10 下午2:00
# @Author  : guowei
# @Site    :
# @File    : template.py
# @Software: PyCharm
import logging
import sqlite3
import time

import itchat
import requests
from bs4 import BeautifulSoup
from flask import json
from itchat.content import *

import job
# filename='info.log',
from template import CoinTemplate

logging.basicConfig(
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S',
    level=logging.DEBUG
)

conn = sqlite3.connect('ai.db')
cursor = conn.cursor()

reply_open = True

help = u'''
start开启 stop停止 其他功能待开发
'''

search_url = 'http://api.feixiaohao.com/search/relatedword?q=%s'
main_page_url = 'http://www.feixiaohao.com/currencies/%s'
main_api_url = 'http://api.feixiaohao.com/currencies/%s'


@itchat.msg_register(TEXT, isFriendChat=True)
def friend_reply(msg):
    text = msg['Text']
    itchat.send(text, toUserName='@51c8c8b3f10630a79716456a82781844')
    return


@itchat.msg_register(TEXT, isGroupChat=True)
def groupchat_reply(msg):
    global reply_open
    text = msg['Text']
    if text == 'stop':
        reply_open = False
        return u'停止工作'
    elif text == 'start':
        reply_open = True
        return u'开始工作'
    elif text == 'help':
        return help

    if not reply_open:
        return
    if text.startswith('AI'):
        send_msg(msg=u'发送一条公告', roomName='AI')
    else:
        if is_alphabet(text[0]) and len(text) < 10:
            result = 'I received: %s' % msg['Text']
            result = getCoinMsg(text)
            return result;
        return


# 判断一个unicode是否是英文字母
def is_alphabet(uchar):
    if (u'\u0041' <= uchar <= u'\u005a') or (u'\u0061' <= uchar <= u'\u007a'):
        return True
    else:
        return False


def getCoinMsg(text):
    result = text + u"价格: "
    url = search_url % text
    search_content = requests.get(url).content
    # logging.debug(search_content)
    coin_list = json.loads(search_content)
    if len(coin_list) > 0:
        coin = coin_list[0]
        name = coin.split('#')[1]
        url = main_page_url % name
        html = requests.get(url).content
        # logging.debug(html)

        soup = BeautifulSoup(html)
        # logging.debug(soup.prettify())
        content = [text for text in soup.select('div.coinprice')[0].strings]
        price = content[0].title()
        logging.debug(price)
        # 涨幅
        increase = content[1].title()
        logging.debug(increase)

        rankx = soup.select('span.tag-marketcap')
        if len(rankx) <= 0:
            return ''
        rank = soup.select('span.tag-marketcap')[0].text
        logging.debug(rank)

        time1 = time.time()
        now = time.strftime("%H:%M:%S", time.localtime(time1))
        logging.debug(now)

        result = CoinTemplate(text.strip(), price, increase, rank, now).__str__()

        return result
    return


# 一定时间获取网站内容，发送到群里
def send_msg(msg, roomName=''):
    time.sleep(2);
    usernameList = []
    if roomName != '':
        rooms = itchat.search_chatrooms(name=roomName)
        logging.debug(rooms)
        username = rooms[0].UserName
        usernameList.append(username)
    else:
        roomList = itchat.get_chatrooms()
        logging.debug(roomList)
        for room in roomList:
            usernameList.append(room.UserName)

    for item in usernameList:
        itchat.send(toUserName=item, msg=msg)


if __name__ == '__main__':
    itchat.config.USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
    itchat.auto_login(enableCmdQR=2, hotReload=True)
    job.job_start()
    itchat.run()
