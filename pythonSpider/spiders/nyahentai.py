# -*- coding: utf-8 -*-
import scrapy

import os, re

from pythonSpider.items import nyahentaiItem

#from pythonSpider.tools.util import createFolder 

class NyahentaiSpider(scrapy.Spider):
    name = 'nyahentai'
    allowed_domains = ['ja.nyahentai.com']
    side_url_code1 = '121750'
    #start_urls = ['http://ja.nyahentai.com/']
    start_urls = ['http://ja.nyahentai.com/g/'+side_url_code1+'/']
    
    def parse(self, response):
        item = nyahentaiItem()
        
        pageCountInfo = response.xpath('//div[@id="info"]/div[1]/text()').extract_first()
        #print(pageCountInfo)
        #print(response.xpath('//div[@id="info"]/div'))        
        pageCount = pageCountInfo.split(' ')[-1] #str
        name = re.sub(r'[,.:]', ' ', response.xpath('//*[@id="info"]/h1/text()').extract_first()) + '[' + pageCount + 'P]'
        
        item['pageCount'] = pageCount
        item['name'] = name
        
        pageOneRelativeUrl = response.xpath('//*[@id="thumbnail-container"]/div[1]/a/@href').extract_first()
        pageOneUrl = response.urljoin(pageOneRelativeUrl)        
        yield scrapy.Request(pageOneUrl, callback=self.parse_pic_url, meta={'item': item}, dont_filter=False)
        
    def parse_pic_url(self, response):
        picSrc = response.xpath('//*[@id="image-container"]/img/@src').extract_first()
        suffix = (picSrc.split('/')[-1]).split('.')[-1]
        preUrl = response.xpath('//*[@id="image-container"]/img/@src').re_first(r'(.*)\d+\.'+suffix+'$')
        
        item = response.meta['item']
        item['preUrl'] = preUrl
        item['suffix'] = suffix
        
        imageUrls = []        
        for index in range(int(item['pageCount'])):
                picUrlFin = item['preUrl'] + str(index+1) + '.' + item['suffix']
                imageUrls.append(picUrlFin)
                #yield scrapy.Request(picUrlFin, callback=self.save_pic, meta={'item': item}, dont_filter=True) #dont_filter=True 此处域名已改变 不为'ja.nyahentai.com'
        item['image_urls'] = imageUrls
        yield item                                                                                               #默认过滤的话，save_pic不会执行

    # def save_pic(self, response):
        # item = response.meta['item']
        # item['path'] = createFolder(item['name'])
        # picName = response.url.split('/')[-1]
        # item['picName'] = picName
        # fullName = os.path.join(item['path'], picName)
        # open(fullName, 'wb+').write(response.body)
        # yield item      