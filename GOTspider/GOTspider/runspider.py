# -*- coding: utf-8 -*-
# @Author: Alan Lau
# @Date  : 2018-03-21 21:44:45

# from scrapy.cmdline import execute
# execute(['scrapy', 'crawl', 'gotspider'])

import os
os.system('scrapy crawl gotspider')
os.system('scrapy crawl contentspider')
