# -*- coding: utf-8 -*-
# @Author: Alan Lau
# @Date  : 2018-03-21 21:46:27

import time
import redis
import scrapy
from lxml import etree
from random import randint
from scrapy.http import Request
from GOTspider.items import GotspiderItem


class spider(scrapy.Spider):
    # def __init__(self):
        # super(spider, scrapy.spider.__init__(*args))
    name = 'gotspider'
    allowed_domains = 'https://www.sbkk88.com'
    bas_url = 'http://www.sbkk88.com/mingzhu/waiguowenxuemingzhu/bingyuhuozhige/'
    tail_url = '.html'

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
            son_url = self.allowed_domains + son_url
            yield Request(url=son_url, callback=self.get_content, meta={'son_url': son_url})

    def get_content(self, response):
        item = GotspiderItem()
        item['url'] = str(response.meta['son_url'])
        selector = etree.HTML(response.text)
        # item['chapter'] =
        pass
