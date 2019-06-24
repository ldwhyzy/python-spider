# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy_redis.spiders import RedisCrawlSpider
from urllib import parse


class AmazonSpider(RedisCrawlSpider):
    name = 'amazon'
    allowed_domains = ['amazon.cn', ]
    #start_urls = ['https://www.amazon.cn/%E5%9B%BE%E4%B9%A6/b/ref=topnav_storetab_b?ie=UTF8&node=658390051', ]
    #redis-cli
    #keys *
    #flushdb
    #lpush amazon:start_urls https://www.amazon.cn/%E5%9B%BE%E4%B9%A6/b/ref=topnav_storetab_b?ie=UTF8&node=658390051
    redis_key = 'amazon:start_urls'

    rules = (
        Rule(LinkExtractor(restrict_xpaths=('//ul[@class="a-unordered-list a-nostyle a-vertical s-ref-indent-one"]/div/li',)), follow=True),
        Rule(LinkExtractor(restrict_xpaths=('//ul[@class="a-unordered-list a-nostyle a-vertical s-ref-indent-two"]/div/li',)), follow=True),
        Rule(LinkExtractor(restrict_xpaths=('//a[@class="a-link-normal s-access-detail-page s-color-twister-title-link a-text-normal"]',)), callback='parse_detail', follow=False),
        Rule(LinkExtractor(restrict_xpaths=('//a[@id="pagnNextLink"]',)), follow=True),
        )
                 
    def parse_detail(self, response):
        item = {}
        item['title'] = response.xpath('//span[@id="productTitle"]/text()').extract_first()
        if not item['title']:
            item['title'] = response.xpath('//span[@id="ebooksProductTitle"]/text()').extract_first().strip()
        item['author'] = response.xpath('//span[@class="author"]/a/text()').extract_first()
        if not item['author']:
            item['author'] = response.xpath('//span[@class="author notFaded"]/a/text()').extract_first()
        #item['desc'] = response.xpath('//h3[@class="productDescriptionSource" and contains(text(), "内容简介")]/../text()').extract()
        item['desc'] = response.xpath('//noscript/div/text()').extract()
        item['desc'] = [i.strip() for i in item['desc'] if len(i.strip())>0]
        print('*'*30, item)
        