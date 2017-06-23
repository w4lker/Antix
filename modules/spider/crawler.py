from v5 import WebkitBrowser 
import multiprocessing
from PyQt5.QtWidgets import QApplication
import sys
from gevent.pool import Pool
from time import time,sleep
import threading
from multiprocessing.dummy import Pool as dummyPool
from gevent import monkey; monkey.patch_os()
from tree import tree
#from common import

class Crawler(): 
    def __init__(self,urls):
        self.urls = urls
    def run(self):
        

        pool = Pool(2)
        pool.map(self.render,self.urls)
    
    def render(self,url):
        w = WebkitBrowser(gui=True)
        w.get(url)
        w.click(pattern='a')
        w.click(pattern='input')
        print w.manager.req_urls
        return True
        #
        
def go(url):
    w = WebkitBrowser(gui=True)
    w.get(url)

    w.click(pattern='input[type=submit]')
    w.click(pattern='input[type=button]')
    w.click(pattern='a')
    #print w.manager.req_urls
    return w.manager.req_urls

class Crawler2(): 
    def __init__(self,url):
        self.urls = [url]
        self.links = [url]
        self.finished = True
        
    def run(self):
        #app = QApplication(sys.argv)
        self.pool =    multiprocessing.Pool(4)
        while True:
            for link in self.links:
                results = self.pool.apply_async(go,(link,),callback=self.render)
                self.links.pop(0)
                if len(self.urls) > 500:
                    self.quit()
                    return
            if len(self.urls) >1 and len(self.links) == 0:
                self.quit()
                #return
                    
    def quit(self):
        t = tree()
        for url in self.urls:
            t.append(url)
        t.printj()
        self.pool.terminate()
        return        
    
    def render(self,result):
        self.finished = False
        print 'callback'
        print result
        self.links.extend(list(set(result).difference(set(self.urls))))
        self.urls = list(set(self.urls).union(set(result)))
        
        #w.click(pattern='a')
        
    #def go(url):
        #w = WebkitBrowser(gui=True)
        #w.get(url)
        #w.click(pattern='a')
        #w.click(pattern='input')
        #print w.manager.req_urls
        #return w.manager.req_urls
    
class Crawler3(): 
    def __init__(self,urls):
        self.urls = urls
        self.pool = dummyPool(10)
        
        
    def run(self):
        url= 'http://news.qq.com'
        w = WebkitBrowser(gui=True)
        result = self.pool.map(w.get,self.urls)
  
        
    
if __name__ == '__main__':
    # initiate webkit and show gui
    # once script is working you can disable the gui
    #app = QApplication(sys.argv)
    start = time()
    #urls = ['http://demo.aisec.cn/demo/aisec/']*10
    urls = 'http://demo.aisec.cn/demo/aisec/'
    c = Crawler2(urls)
    c.run()
    end = time()
    print end -start