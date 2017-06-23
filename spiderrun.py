#from modules.spider import webspider

#from modules import spider

#if __name__ == '__main__':
    #'''
    #settings = Settings()
    #s = Crawler(TestSpider,settings)
    #s.crawl()
    #'''
    #settings = Settings()
    #settings.set("USER_AGENT", "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0")
    #settings.set("DOWNLOAD_TIMEOUT",5)
    #print settings
    #process = CrawlerProcess(settings)
    #process.crawl(WebSpider)
    #process.start()

from modules.spider.v5 import *
from multiprocessing.dummy import Pool as ThreadPool 
#if __name__ == '__main__':
        #url=['http://demo.aisec.cn/demo/aisec/']
        #c = Crawler(url,poolSize=100,pageNum=2000)
        #c.run()
        #print c.urls
        #c.tree.printj()
if __name__ == '__main__':
        url=['http://demo.aisec.cn/demo/aisec/','http://www.hnust.cn']
        c = Crawler(url)
        print c.urls
        
