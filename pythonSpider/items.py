# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PythonspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #pass
    name = scrapy.Field()
    title = scrapy.Field()
    info = scrapy.Field()
    
class nyahentaiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #pass
    name = scrapy.Field()
    pageCount = scrapy.Field()
    preUrl = scrapy.Field()
    suffix = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()    
    #image_paths = scrapy.Field()    
    
class jdBookItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #pass
    name = scrapy.Field()
    price = scrapy.Field()
    desc = scrapy.Field()
    first_class = scrapy.Field()
    second_class = scrapy.Field()
    image_url = scrapy.Field()    
    #image_paths = scrapy.Field()     
    
class DangdangbookItem(scrapy.Item):    
    title = scrapy.Field()
    author = scrapy.Field()
    first_level = scrapy.Field()
    second_level = scrapy.Field()
    third_level = scrapy.Field()
    price = scrapy.Field()
    des = scrapy.Field()    