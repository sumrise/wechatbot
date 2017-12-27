#!python3
# coding=UTF-8

import logging
import threading

import requests

from model import Notice
from bs4 import BeautifulSoup
from tgbot import send_msg

from template import NoticeTemplate

logging.basicConfig(level=logging.DEBUG)

home_url = 'http://www.feixiaohao.com/notice/'
bishijie_url = 'http://m.bishijie.com/kuaixun/?from=groupmessage&isappinstalled=0'


def getFeixiaohao():
    html = requests.get(home_url).content
    soup = BeautifulSoup(html)
    abcx = soup.select('ul.noticeList li')
    if len(abcx) <= 0:
        return ''
    abc = soup.select('ul.noticeList li')[0]

    platform = abc.select('a')[0].get_text()
    title = abc.select('a')[1]['title']
    # url = abc.select('a')[1]['href']
    date = abc.select('a span')[0].get_text()
    source = 'feixiaohao'

    return Notice(platform=platform, title=title, url='', date=date, source=source)


def getBishijie():
    html = requests.get(bishijie_url).content
    soup = BeautifulSoup(html)
    article = soup.select('article')[0]

    platform = u'币市快讯'
    title = article.select('p')[0].get_text()
    url = ''
    date = soup.select('h2')[1].get_text().lstrip() + article.select('h3')[0].get_text()
    source = 'bishijie'

    return Notice(platform=platform, title=title, url=url, date=date, source=source)


# 定时根据数据库里的platform 抓取notice
def getPlatformNotice(func):
    notice = func()
    noticeList = Notice.select().where(Notice.source == notice.source)
    insert = True
    if len(noticeList) > 0:
        for no in noticeList:
            if no.title[0:10] == notice.title[0:10]:
                insert = False
                logging.debug(no.title[0:10] + 'equals' + notice.date)

    if insert is True:
        result = Notice.delete().where(Notice.source == notice.source)
        result.execute()

        logging.debug('delete success')
        # result = Notice.insert(notice)
        notice.save()
        # result.execute()

        result = NoticeTemplate(notice).__str__()
        success = send_msg(text=result)  # coin

        logging.info(success)


def fun_timer():
    getPlatformNotice(getFeixiaohao)
    getPlatformNotice(getBishijie)
    global timer
    timer = threading.Timer(60, fun_timer)
    timer.start()


def job_start():
    timer = threading.Timer(10, fun_timer)
    timer.start()


if __name__ == '__main__':
    job_start()
    logging.info("Start Job! -------------")
