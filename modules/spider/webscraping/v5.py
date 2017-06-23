#!/usr/bin/env python

#coding: utf-8


import sys
import re
import time
from lxml import html
#from libs.urllibs import *
#from libs.tree import *
#from PyQt4.QtCore import SIGNAL, QUrl, QSize

from PyQt5.QtCore import QUrl,QSize,pyqtSignal,QThread,QEventLoop,QThreadPool,Qt
from PyQt5.QtWebKitWidgets import QWebFrame, QWebPage, QWebView
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebKit import QWebSettings,QWebHistory
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest,QNetworkDiskCache,QNetworkReply
from functools import partial



reload(sys)
sys.setdefaultencoding('utf-8')


class Render(QWebPage):

    def __init__(self, url):
        self.url = url
        self.app = QEventLoop()
        QWebPage.__init__(self)
        self.urls = []
        self.frame = self.mainFrame()
        self.viewport = self.setViewportSize(QSize(1600, 9000))
        self.network = NetworkAccessManager()
        self.setNetworkAccessManager(self.network)
        self.loadFinished.connect(self._loadFinished)
        self.linkClicked.connect(self.linkClick)
        self.settings().setAttribute(QWebSettings.AutoLoadImages,False)
        self.settings().setAttribute(QWebSettings.JavascriptCanOpenWindows,False)
        self.setLinkDelegationPolicy(2)
        #self.action(QWebPage.OpenLinkInNewWindow).setEnabled(True) 
        #self.settings().clearMemoryCaches()
        self.mainFrame().load(QUrl(self.url))
        self.network.requestSignal.connect(self.networkRequest)
        self.app.exec_()

    allFinished = pyqtSignal()   
    def _loadFinished(self, res):
        iList = self.frame.findAllElements('input')

        for i in iList:
            i.evaluateJavaScript('this.click()')

        aList = self.frame.findAllElements('a')
        for a in aList:
            a.evaluateJavaScript('this.click()')
     
        
        
    
        if self.frame.blockSignals(True) == True:
            self.isFinished = True
            self.allFinished.emit()
            self.app.quit()
            self.deleteLater()

        
        
    def javaScriptAlert(browser, frame, message):
        """Notifies session for alert, then pass."""
        print "signal for javaScriptAlert (class) fired"
    
    def javaScriptConfirm(browser, frame, message):
        #"""Notifies session for alert, then pass."""
        print "signal for javaScriptConfirm (class) fired"
    
    def javaScriptPrompt(browser, frame, message):
        #"""Notifies session for alert, then pass."""
        print "signal for javaScriptPromt (class) fired"        
    
    def networkRequest(self):
        self.urls = self.network.request_urls
        print self.network.request_urls
        print 'allfinished'
   
    def linkClick(self,url):
        self.urls.append(url.url())



        
class NetworkAccessManager(QNetworkAccessManager):
    def __init__(self):
        super(NetworkAccessManager, self).__init__()
        self.finished.connect(self.finishd)

        self.request_urls = []
        self.replys = []
        self.ban = (
            '.*\.css',
            '.*\.jpg',
            '.*\.png',
        )
    requestSignal = pyqtSignal()
    def createRequest(self, operation, request, data):
        url = str(request.url().toString())
        self.request_urls.append(url)
        print 'requesting:'+url
        if re.search('.*\.css', url):
            self.setNetworkAccessible(QNetworkAccessManager.NotAccessible)
        else:
            self.setNetworkAccessible(QNetworkAccessManager.Accessible)
        self.requestSignal.emit()
        
        reply = QNetworkAccessManager.createRequest(self, operation,request, data)
        reply.readyRead.connect(lambda:self.ready_read(reply))
        reply.finished.connect(lambda:self.ajax_read(reply))
        #self.replys.append(reply)
        return reply
    
    def post(request,data):
        url = str(request.url().toString())
        self.request_urls.append(url)
        print 'post:'+url        
    
    def ready_read(self,reply):
        print 'active request:'
        #url = str(reply.url().toString())
        #hrefs = get_atts(url,reply.peek(102400).data(),'//a/@href')
        #self.check_exists(hrefs)
    
    def ajax_read(self,reply):
        print 'ajax:'
        #url = str(reply.url().toString())
        #hrefs = get_atts(url,reply.peek(102400).data(),'//a/@href')
        #self.check_exists(hrefs)        

    
    def finishd(self, reply):
        print 'In NetworkAccessManager finishd'
        url = str(reply.url().toString())
        #print self.request_url
        #print url
    
    def check_exists(self,hrefs):
        for href in hrefs:
            if href not in self.request_urls:
                self.request_urls.append(href)

class Crawler():
    def __init__(self,websites,poolSize=10,pageNum=200):
        self.pageNum = pageNum
        self.tree = tree()
        self.websites = []
        for site in websites:
            self.websites.append(get_netloc(site))
        self.links = websites

        self.urls = []  
        self.poolSize = poolSize
        self.pool = []
        self.app = QApplication(sys.argv)
        
    def remove(self,r):
        print 'remove'
        self.pool.remove(r)
        return r
    
    def run(self):
        while(True):


            while self.pool.count(None) > 0:
                self.pool.remove(None)
                
            for link in self.links:
                if get_netloc(link) not in self.websites:
                    self.links.remove(link)
                    continue
                if link not in self.urls:
                    if len(self.urls)>self.pageNum:
                        print self.urls
                        self.app.quit()
                        return                     
                    if len(self.pool) <= self.poolSize:
                        self.tree.append(link)
                        self.urls.append(link)
                        self.links.remove(link)
                        r = Render(link)
                        self.pool.append(r)
                        r.allFinished.connect(partial(self.remove,r))
                        for u in r.urls:
                            if u not in self.urls:
                                self.links.append(u)
                    else:
                        self.removePool()
                else:
                    self.links.remove(link)
            if len(self.links) == 0:
                return

        
                       
            
        #self.qwebframe.load(self.qurl)
    
    def removePool(self):
        for r in self.pool:
            if r.isFinished == True:
                self.pool.remove(r)
                del r

#if __name__ == '__main__':
    #url='http://demo.aisec.cn/demo/aisec/'
    #c = Crawler(url,10)
    #c.run()
    #del r
#def remove(r):
    #print 'remove'
    #return 


if __name__=='__main__':
    url = 'http://demo.aisec.cn/demo/aisec/'
    app = QApplication(sys.argv)
    r = Render(url)
    ##r.allFinished.connect(remove(r))
    print r.urls
    #print r
    #app.exec_()
    #app.quit()
    #del r
    #$print r.urls


