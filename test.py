#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/11/9 下午5:40
# @Author  : Aries
# @Site    : 
# @File    : test.py
# @Software: PyCharm


# !/usr/bin/env python
# -*- coding:utf-8-*-
import requests
from bs4 import BeautifulSoup

bishijie_url = 'http://m.bishijie.com/kuaixun/?from=groupmessage&isappinstalled=0'

if __name__ == "__main__":
    html = requests.get(bishijie_url).content
    soup = BeautifulSoup(html)
    article = soup.select('article')[0]

    date = soup.select('h2')[1].get_text().lstrip() + article.select('h3')[0].get_text()
    title = article.select('p')[0].get_text()
    platform = u'币世界快讯'
    url = ''
