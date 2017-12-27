#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/11/10 下午2:00
# @Author  : Aries
# @Site    : 
# @File    : template.py
# @Software: PyCharm
result_template = u'''
币安网的%s价格:%s
涨幅:%s
市值排名：%s
【%s】
'''

result_notice_template = u'''
%s
%s
%s
%s
'''


class NoticeTemplate():
    def __init__(self, platform, title, url, date):
        self.platform = platform
        self.title = title
        self.url = url
        self.date = date

    def __init__(self, notice):
        self.platform = notice.platform
        self.title = notice.title
        self.url = notice.url
        self.date = notice.date

    def __str__(self):
        return result_notice_template % (
            self.platform,
            self.title,
            self.url,
            self.date
        )


class CoinTemplate():
    def __init__(self, name, price, increase, rank, now):
        self.name = name
        self.price = price
        self.increase = increase
        self.rank = rank
        self.now = now

    def __str__(self):
        return result_template % (
            self.name,
            self.price,
            self.increase,
            self.rank,
            self.now
        )


if __name__ == '__main__':
    print(type(result_template))
    template = CoinTemplate(name=u'hsr', price=u'￥12', increase=u'123%', rank=u'第12名', now=u'14:02')
    print(template.__str__())

    notice = NoticeTemplate(platform='kubi', title='abc', url='http', date='09:13')
    print(notice.__str__())

    # rank=u'第12名'.encode('utf-8')
