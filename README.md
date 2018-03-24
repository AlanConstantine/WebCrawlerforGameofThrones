# Scrapy+redis+mongodb分布式爬虫抓取《冰与火之歌》

#### 技术栈
* Scrapy
* redis
* mongodb
* xpath

#### 环境
* python3.5.2
* ubuntu 16.04LTS

#### 思路
master只需要准备redis，slave先将所有的小说章节界面的url抓取下来，通过redis发动到master的内存，再由master分配任务给slave，实现分布式

#### 运行
* 执行runspider.py
* master地址在setting.py设置
