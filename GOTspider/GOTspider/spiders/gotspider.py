# -*- coding: utf-8 -*-
# @Author: Alan Lau
# @Date  : 2018-03-21 21:46:27

import redis
import scrapy
from lxml import etree
from random import randint
from scrapy.http import Request
from GOTspider.items import UrlItem
from scrapy_redis.spiders import RedisSpider


class Spider(scrapy.Spider):
    name = 'gotspider'
    custom_settings = {
        'ITEM_PIPELINES': {
            'GOTspider.pipelines.RedisPipeline': 300
        }}
    main_url = 'https://www.sbkk88.com'
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
        # item = UrlItem()
        for son_url in son_urls:
            item = UrlItem()
            son_url = self.main_url + son_url
            item['url'] = son_url
            yield item

    # def parse(self, response):
    #     selector = etree.HTML(response.text)
    #     son_urls = selector.xpath(
    #         '//div[@class="mingzhuMain"]/div[@class="mingzhuLeft"]/ul[@class="leftList"]/li/a/@href')
    #     for son_url in son_urls:
    #         son_url = self.main_url + son_url
    #         yield Request(son_url, self.get_content, meta={'son_url': son_url})

    # def get_content(self, response):
    #     item = GotspiderItem()
    #     item['url'] = str(response.meta['son_url'])
    #     selector = etree.HTML(response.text)
    #     item['chapter'] = selector.xpath('//div[@id="f_title1"]/h1/text()')[0]
    #     content = ''.join(list(map(lambda p: p.strip(), selector.xpath(
    #         '//div[@id="f_content1"]/div[@id="f_article"]/p/text()'))))
    #     item['content'] = content
    #     characters = []
    #     for row in self.characterlists:
    #         for role in row:
    #             if role in content:
    #                 characters.append(row[0])
    #     item['characters'] = '/'.join(list(set(characters)))
    #     yield item
