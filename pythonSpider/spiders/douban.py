# -*- coding: utf-8 -*-
import scrapy
import re


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['douban.com']
    start_urls = ['https://www.douban.com/people/71814315/',
                  'https://accounts.douban.com/j/mobile/login/basic']
    
    # def start_requests(self):
        # cookies = 'bid=MRilYHiU2uA; __yadk_uid=36jAGvKgBXUJTiXwMtNjpZW3gqhyWC4S; _vwo_uuid_v2=D1A7CF7EFBF5663C1FC5623720C0F3DC5|e03c64d61e277b4c3004a918ef786b94; \
        #    gr_user_id=fa831861-d2c6-4136-b011-479eb27857c7; douban-fav-remind=1; ll="108258"; trc_cookie_storage=taboola%2520global%253Auser-id%3D70e8866b-b389-4888-b618-536e740cfe12-tuct27301be; \
        #    __utmc=30149280; __utmz=30149280.1559880165.51.49.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; dbcl2="71814315:7/IeyGDlGtY"; ck=y_wj; ap_v=0,6.0; push_noty_num=0; push_doumail_num=0; \
        #    __utmv=30149280.7181; douban-profile-remind=1; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1559886960%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3Dj_mB31S4OEu3x-SKCPuD_NsTmu-Otm3xImHKL2fHH4y%26wd%3D%26eqid%3D985a31f70017df0c000000065cf9e1d1%22%5D; \
        #    _pk_ses.100001.8cb4=*; __utma=30149280.728640247.1541087449.1559880165.1559886961.52; __utmt=1; __utmb=30149280.4.10.1559886961; _pk_id.100001.8cb4=55f1ec7bb4062904.1530623270.19.1559887022.1559880517.'
        # cookies = {i.split("=")[0]:i.split("=")[1] for i in cookies.split('; ')}
        # yield scrapy.Request(self.start_urls[0], callback=self.parse, cookies=cookies)
        
    def start_requests(self):
        yield scrapy.FormRequest(self.start_urls[1], 
            formdata=dict(name='xxxxxxxxx', password='monsterxxxx'), callback=self.parse)            

    def parse(self, response):
        print(response.url, response.status)
        #print(response.url, response)
        print(re.findall(r"ldzy", response.body.decode()))
        url = 'https://www.douban.com/mine/'
        yield scrapy.Request(url, callback=self.parse_details)
        
    def parse_details(self, response):
        #wanted = response.xpath('//li[@class="aob"]/a/@title/text()').extract()
        wanted = response.xpath('//li[@class="aob"]/a/@title').extract()
        with open('a.html', 'w', encoding='utf-8') as f:
            f.write(response.body.decode())
        print(re.findall(r"Пл¶Б", response.body.decode()))    
        for i in wanted:
            print(i)
            