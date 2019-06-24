# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider
from pythonSpider.items import DangdangbookItem
import copy

class DangdangSpider(RedisSpider):
    name = 'dangdang'
    allowed_domains = ['dangdang.com']
    redis_key = 'dangdang:start_urls' 
    #start_urls = ['http://dangdang.com/']

    # def __init__(self, *args, **kwargs):
        # # Dynamically define the allowed domains list.
        # domain = kwargs.pop('domain', '')
        # self.allowed_domains = filter(None, domain.split(','))
        # super(DangdangSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        item = DangdangbookItem()
        first_levels = response.xpath('//div[contains(@class, "first_level ")]')
        
        for first_level in first_levels:
            first_level_line = first_level.xpath('./a/h3/text()')
            if first_level_line:
                item['first_level'] = first_level_line.extract_first().replace('/', ' ')
                #logger.warning('*'*30)
                #logger.warning(item['first_level'])
                second_level_lines = first_level.xpath('./ul/li')
                for second_level_li in second_level_lines:
                    item['second_level'] = second_level_li.xpath('./a/h4/text()').extract_first().replace('/', ' ')
                    third_level_lis = second_level_li.xpath('./ul')
                    if not third_level_lis.xpath('./a'):
                        url = second_level_li.xpath('./a/@href').extract_first()
                        item['third_level'] ='无'
                        yield scrapy.Request(url, callback=self.parse_book_details, meta={'item':copy.deepcopy(item)})
                    else:
                        for third_level_li in third_level_lis:
                            item['third_level'] = third_level_li.xpath('./a/li/text()').extract_first()    
                            url = third_level_li.xpath('./a/@href').extract_first()
                            yield scrapy.Request(url, callback=self.parse_book_details, meta={'item':copy.deepcopy(item)})
                      
    def parse_book_details(self, response):
        item = response.meta['item']    
        book_lists = response.xpath('//div[@class="book book_list clearfix"]/a/div[@class="bookinfo"]')
        for book_info in book_lists:
            item['title'] = book_info.xpath('./div[@class="title"]/text()').extract_first()
            item['author'] = book_info.xpath('./div[@class="author"]/text()').extract_first()
            item['price'] = book_info.xpath('./div[@class="price"]/span/text()').extract_first()
            item['des'] = book_info.xpath('./div[@class="des"]/text()').extract_first().replace('\u3000', '').replace('\xa0', '').strip()
            yield item