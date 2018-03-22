# -*- coding: utf-8 -*-
# @Author: Alan Lau
# @Date  : 2018-03-21 21:46:27

import time
import xlrd
import redis
import scrapy
from lxml import etree
from random import randint
from scrapy.http import Request
from GOTspider.items import GotspiderItem


class Spider(scrapy.Spider):
    name = 'gotspider'
    main_url = 'https://www.sbkk88.com'
    bas_url = 'http://www.sbkk88.com/mingzhu/waiguowenxuemingzhu/bingyuhuozhige/'
    tail_url = '.html'

    def __init__(self):
        self.characterlists = []
        with open(r'../../roles.txt', 'r') as f:
            lines = f.readlines()
        for line in lines:
            self.characterlists.append((line.strip()).split('\t'))
        print(self.characterlists)

    def start_requests(self):
        for i in range(1, 6):
            url = self.bas_url + 'b' + str(i) + '/'
            yield Request(url, self.parse)
        # http://www.sbkk88.com/mingzhu/waiguowenxuemingzhu/bingyuhuozhige/b1/

    def parse(self, response):
        selector = etree.HTML(response.text)
        son_urls = selector.xpath(
            '//div[@class="mingzhuMain"]/div[@class="mingzhuLeft"]/ul[@class="leftList"]/li/a/@href')
        for son_url in son_urls:
            son_url = self.main_url + son_url
            yield Request(son_url, self.get_content, meta={'son_url': son_url})

    def get_content(self, response):
        item = GotspiderItem()
        item['url'] = str(response.meta['son_url'])
        selector = etree.HTML(response.text)
        item['chapter'] = selector.xpath('//div[@id="f_title1"]/h1/text()')[0]
        content = ''.join(selector.xpath(
            '//div[@id="f_content1"]/div[@id="f_article"]/p/text()'))
        item['content'] = content
        characters = []
        for row in self.characterlists:
            for role in row:
                if role in content:
                    characters.append(row[0])
        item['characters'] = list(set(characters))
        yield item
