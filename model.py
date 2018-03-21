# -*- coding: utf-8 -*-
# @Date     : 2017-04-07 10:16:53
# @Author   : Alan Lau (rlalan@outlook.com)
# @Language : Python3.5

from peewee import *
from datetime import datetime

db = SqliteDatabase(r'A_Song_of_Ice_and_Fire.sqlite')
# 建立名字为A_Song_of_Ice_and_Fire.sqlite的数据库


class BaseModel(Model):

    class Meta:
        database = db


class novel(BaseModel):
    id = IntegerField(primary_key=True, verbose_name='id')
    # 数据id
    chapter = CharField(max_length=20, null=True, verbose_name='chapter')
    # 文本章节
    title = CharField(max_length=500, null=True, verbose_name='title')
    # 章节标题
    content = TextField(null=True, verbose_name='content')
    # 章节内容
    characters = CharField(max_length=200, null=True,
                           verbose_name='characters')
    # 章节中出现的演员
    url = CharField(max_length=200, null=False, verbose_name='url')
    # 章节的url，方便出错后重爬
    created_at = DateTimeField(
        default=datetime.now(), null=True, verbose_name='Get_time')
    # 产生日期


if __name__ == '__main__':
    try:
        novel.create_table()
    except Exception as err:
        print(err)
