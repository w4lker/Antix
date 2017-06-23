#from scrapy.crawler import Crawler
#from scrapy.crawler import CrawlerProcess
#from scrapy.settings import Settings
#from scrapy import Spider
#from scrapy import Request
#from scrapy.selector import Selector
from libs.db import *
from libs.tree import *
from libs.urllibs import *
import os

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class WebSpider(Spider):
    name = 'webspider'
    start_urls = ['http://211.67.208.108:8080/xy/home.do?method=index']
    url_list = []
    login_url = ['login','signin']
    uploud_url = ['upload']
    #allowed_domains = ["211.67.208.108:8080"]
    form_names = ['passwd','password']
    filter_hrefs = [u'/',u'javascript:void(0)','#','./']
    ignore_exts = ['exe','jpg','gif','bmp','swf']
    url_tree = tree()
    f = open('url.txt','w')
    '''
    def start_requests(self):
        print 'hello'
        return [Request("https://blog.scrapinghub.com",callback=self.parse)]
    '''
    def parse(self, response):
        print response.url
        #Selector(response)
        if response.headers['content-type'].split(';')[0] != "text/html":
            return
        
        select('test',a=1)
        hrefs = response.xpath('//a/@href').extract()
        types = response.xpath('//input/@type').extract()
        
        filename = get_filename(response.url)
        #if filename != '':
            #self.url_tree.get(filename)['url'] = response.url
        if 'password' in types:
            self.url_tree.set(response.url,password='true')
        
        if 'file' in types:
            self.url_tree.set(response.url,file='true')            
        
        
        for href in hrefs:
            if href not in self.filter_hrefs:
                
                
                url = response.urljoin(href)
                
                if url not in self.url_list:
                    self.url_list.append(url)
                    self.f.write(url + u'\n')
                    self.url_tree.append(url)
                    ext = get_ext(href)
                    if ext in self.ignore_exts:
                        return                    
                    yield Request(url,callback=self.parse)      #µ›πÈ≈¿»°
        
    def close(self,spider, reason):
        self.url_tree.printj()
        Spider.close(spider, reason)
        
    

                    


if __name__ == '__main__':
    '''
    settings = Settings()
    s = Crawler(TestSpider,settings)
    s.crawl()
    '''
    settings = Settings()
    settings.set("USER_AGENT", "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0")
    settings.set("DOWNLOAD_TIMEOUT",5)
    print settings
    process = CrawlerProcess(settings)
    process.crawl(WebSpider)
    process.start()
    