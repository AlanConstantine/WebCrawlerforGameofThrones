# -*- coding: utf-8 -*-
# @Date     : 2017-04-07 10:15:04
# @Author   : Alan Lau (rlalan@outlook.com)
# @Language : Python3.5

from bs4 import BeautifulSoup
import requests
import time
import random
import reader
from model import novel
import numpy as np


def log(func):
    def wrapper(*args, **kwargs):
        wait = random.randint(3, 10)
        print('------------------Sleep %ss----------------------' % str(wait))
        print('%s is called.' % func.__name__)
        re = func(*args, **kwargs)
        time.sleep(wait)
        return re
    return wrapper


@log
def get_html(url, characters_data):
    try:
        id = int(time.time())
        html = requests.get(url, timeout=5)
        html.encoding = 'gb2312'
        soup = BeautifulSoup(html.text, "html.parser")

        title = (soup.find('h1').string).split(' ')

        p = soup.find_all('p')
        content = ''
        for ech_p in p:
            txt = ech_p.string
            if str(type(txt)) == "<class 'NoneType'>":
                continue
            content = content+ech_p.string+'/'

        character_list = []

        for ech_character in characters_data:
            content = content.replace(ech_character[1], ech_character[0]).replace(
                ech_character[2], ech_character[0])
            # print(ech_character[0])
            if ech_character[0] in content:
                # print(ech_character[0])
                character_list.append(ech_character[0])
            else:
                continue

        character_set = list(set(character_list))
        print(character_set)
        character = '/'.join(character_set)
        if len(title) == 1:
            chapter = '序章'
            title_txt = ''
        else:
            chapter = title[-2]
            title_txt = title[-1]
        novel.create(id=id, chapter=chapter,
                     title=title_txt, content=content[:-1], url=url, characters=character)
    except Exception as e:
        print(e)
        raise
    else:
        pass
    finally:
        pass


def main():
    page_range = (np.arange(149481, 149550+1, 1, dtype=int))[::-1]
    character_path = r'角色表.xlsx'
    characters_data = reader.readxls(character_path)[1:]
    vol = 'b5'
    for page in page_range:
        print(page)
        url = 'http://www.sbkk88.com/mingzhu/waiguowenxuemingzhu/bingyuhuozhige/%s/%s.html' % (vol, str(
            page))
        get_html(url, characters_data)


if __name__ == '__main__':
    main()
