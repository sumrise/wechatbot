#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/27 下午3:34
# @Author  : guowei
# @Site    : 
# @File    : home_test.py
# @Software: PyCharm





import requests
import time

while True:
    time.sleep(10)
    try:
        content = requests.get('http://www.geek-wemedia.com')
        # content = content.content
        print(content.content)

    except Exception as e:
        print(e)
