# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem

from pythonSpider.tools import util

# class PythonspiderPipeline(object):
    # def process_item(self, item, spider):
        # #print('pipleline******************')
        # #print(item['path'])
        # return item
        
class NyahentaiSpiderPipeline(ImagesPipeline):            
    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url, meta={'item':item})  
            
    def file_path(self, request, response=None, info=None):
        item= request.meta['item']
        name = util.pathValidate(item['name'])
        fullName = name+'/'+request.url.split('/')[-1]
        return fullName        

    # def item_completed(self, results, item, info):
        # image_paths = [x['path'] for ok, x in results if ok]
        # if not image_paths:
            # raise DropItem("Item contains no images")
        # item['image_paths'] = image_paths
        # return item       
        
class JdSpiderPipeline(object):
    def process_item(self, item, spider):
        #print(item)
        return item     

class DangdangSpiderPipeline(object):
    def process_item(self, item, spider):
        #print(item)
        return item           
        
        