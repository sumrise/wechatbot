#!python2.6
# coding=UTF-8

from peewee import *

db = SqliteDatabase('ai.db')


class Notice(Model):
    platform = CharField()
    url = CharField()
    title = CharField()
    date = CharField()
    source = CharField()

    class Meta:
        database = db
