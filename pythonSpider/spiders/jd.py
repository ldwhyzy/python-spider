# -*- coding: utf-8 -*-
import scrapy
import copy
from urllib import parse
from pythonSpider.items import jdBookItem
import json, re


class JdSpider(scrapy.Spider):
    name = 'jd'
    allowed_domains = ['jd.com', 'p.3.cn', 'dx.3.cn']
    start_urls = ['https://book.jd.com/booksort.html']

    def parse(self, response):
        dt_list = response.xpath('//div[@class="mc"]/dl/dt')        
        for dt in dt_list:
            item = {}
            item['first_class'] = dt.xpath('./a/text()').extract_first()
            em_list = dt.xpath('./following-sibling::dd[1]/em')
            for em in em_list:
                item['second_class'] = em.xpath('./a/text()').extract_first()
                list_url = em.xpath('./a/@href').extract_first()
                list_url = parse.urljoin(self.start_urls[0], list_url)
                #print(list_url)
                yield scrapy.Request(list_url, callback=self.books_info, meta={'item':copy.deepcopy(item)})
        
    def books_info(self, response):
        item = response.meta['item']
        li_list = response.xpath('//li[@class="gl-item"]')
        #'''
        for li in li_list:
            item['name'] = li.xpath('//div[@class="p-name"]/a/em/text()').extract_first().strip()
            item['author'] = li.xpath('//*[@class="author_type_1"]/a/@title').extract_first()
            item['press'] = li.xpath('//*[@class="p-bi-store"]/a/@title').extract_first()
            sku_id = li.xpath('.//div/@data-sku').extract_first()
            yield scrapy.Request('https://p.3.cn/prices/mgets?skuIds=J_{}'.format(sku_id), 
                callback=self.get_price, meta={'item': copy.deepcopy(item)})   
            book_url = li.xpath('//div[@class="p-name"]/a/@href').extract_first()
            book_url = parse.urljoin(self.start_urls[0], book_url)
            #print('*'*30)
            #print(book_url)
            #yield scrapy.Request(book_url, callback=self.book_detail, meta={'item': copy.deepcopy(item)})
        #'''
        next_page_url = response.xpath('//a[@class="pn-next"]/@href').extract_first()
        if next_page_url:
            next_page_url = parse.urljoin(response.url, next_page_url)   
            yield scrapy.Request(next_page_url, callback=self.books_info, meta={'item': copy.deepcopy(item)})            
        #'''
    def get_price(self, response):
        item = response.meta['item']
        item['price'] = json.loads(response.body.decode())[0]['op']
        yield item
         
    def book_detail(self, response):
        item = response.meta['item']
        info = response.xpath('//div[@class="itemInfo"]')
        item['desc'] = response.xpath('//div[@class="book-detail-content"]/text()').extract_first().strip()
        #yield item
        print('*'*30)
        print(item)