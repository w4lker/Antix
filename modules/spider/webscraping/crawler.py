from webkit import WebkitBrowser
#from v5 import Render 
import multiprocessing
from PyQt4.QtGui import QApplication
#from PyQt5.QtWidgets import QApplication
import sys
#from gevent.pool import Pool
from time import time

def go(url):
    w = WebkitBrowser(gui=False)
    w.get(url)
    print 'click'
    w.click(pattern='input')
    w.click(pattern='a')
    return w.manager.req_urls
#    return w.page().networkAccessManager().req_urls

class Crawler(): 
    def __init__(self,urls):
        self.urls = urls
        self.pool =    multiprocessing.Pool(2)
    def run(self):
        #app = QApplication(sys.argv)
        
        results = self.pool.map(go,self.urls)

        self.pool.close()
        self.pool.join()
        print 'quit'
        print results

class Crawler2(): 
    def __init__(self,urls):
        self.urls = urls
        self.pool = Pool(10)
        
    def run(self):
        w = WebkitBrowser(gui=True)
        results=self.pool.map(w.get, self.urls)
        print results
        #w.close()
        return True

class Crawler3(): 
    def __init__(self,urls):
        self.urls = urls
        self.pool = multiprocessing.Pool(10)
        
        
    def run(self):
        results = []
        for url in self.urls:
            results.append(self.pool.apply_async(go,args=(url,)))
        self.pool.close()
        self.pool.join()
        print results
  
        
    
if __name__ == '__main__':
    # initiate webkit and show gui
    # once script is working you can disable the gui
    #app = QApplication(sys.argv)
    start = time()
    urls = ['http://demo.aisec.cn/demo/aisec/']*2
    c = Crawler(urls)
    b = c.run()
    end = time()
    print end-start