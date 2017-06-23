#!/usr/bin/env python

#coding: utf-8


import sys
import re
import time

#from PyQt4.QtCore import SIGNAL, QUrl, QSize

from PyQt5.QtCore import QUrl,QSize,pyqtSignal,QThread,QEventLoop
from PyQt5.QtWebKitWidgets import QWebFrame, QWebPage, QWebView
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebKit import QWebSettings,QWebHistory
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest,QNetworkDiskCache,QNetworkReply
import time

reload(sys)
sys.setdefaultencoding('utf-8')


class Render(QWebPage):

    def __init__(self, url):
        self.url = url
        self.app = QEventLoop()
        QWebPage.__init__(self)
        self.urls = [url]
        self.frame = self.mainFrame()
        self.viewport = self.setViewportSize(QSize(1600, 9000))
        self.network = NetworkAccessManager()
        self.setNetworkAccessManager(self.network)
        self.loadFinished.connect(self._loadFinished)
        self.linkClicked.connect(self.change)
        self.settings().setAttribute(QWebSettings.AutoLoadImages,False)
        self.settings().setAttribute(QWebSettings.JavascriptCanOpenWindows,True)
        self.setLinkDelegationPolicy(1)
        self.action(QWebPage.OpenLinkInNewWindow).setEnabled(True) 
        #self.settings().clearMemoryCaches()
        #self.mainFrame().load(QUrl(self.url))
        self.network.requestSignal.connect(self.networkRequest)
        self.thread = QThread()
        self.moveToThread(self.thread)
        self.thread.started.connect(self.run)
        self.thread.run()

    def run(self):
        self.mainFrame().load(QUrl(self.urls.pop(0)))
        self.app.exec_()
        
    def _loadFinished(self, res):
        ilist = self.frame.findAllElements('input')
        for i in ilist:
            i.evaluateJavaScript('this.click()')
            print i.attribute("onClick")
            #self.setLinkDelegationPolicy(QWebPage.DelegateAllLinks)
        #self.setLinkDelegationPolicy(0)
        alist = self.frame.findAllElements('a')
        for a in alist:
            a.evaluateJavaScript("this.click()")
    
        

        if self.frame.blockSignals(True) == False:
            print 'yes'
            self.app.quit()
        
        
    def javaScriptAlert(browser, frame, message):
        """Notifies session for alert, then pass."""
        print "signal for javaScriptAlert (class) fired"
        
    
    def networkRequest(self):
        self.urls = self.network.request_Urls    
        print 'allfinished'
        
    def change(self,url):
        self.urls.append(url.url())
        print url.url()
        #self.setLinkDelegationPolicy(0)
        print 'change'

        
class NetworkAccessManager(QNetworkAccessManager):
    def __init__(self):
        super(NetworkAccessManager, self).__init__()
        self.finished.connect(self.finishd)

        self.request_Urls = []
        self.replys = []
        #self.reply.finished.connect(self.finishd)
        cache = QNetworkDiskCache()
        cache.setCacheDirectory('.cache')
        cache.setMaximumCacheSize(1 * 1024 * 1024) # need to convert cache value to bytes
        self.setCache(cache)
        #self.SIGNAL.connect(self.finished)
        self.ban = (
            '.*\.css',
            '.*\.jpg',
            '.*\.png',
        )
    requestSignal = pyqtSignal()
    def createRequest(self, operation, request, data):
        url = str(request.url().toString())
        self.request_Urls.append(url)
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
    
    def ready_read(self,reply):
        print 'haha'
        #print reply.peek(102400)
    
    def ajax_read(self,reply):
        print 'aa'
        #print 'ajax' + reply.peek(102400)    
    
    def finishd(self, reply):
        print 'In NetworkAccessManager finishd'
        url = str(reply.url().toString())
        #print self.request_url
        #print url

class Crawler():
    def __init__(website):
        self.website = website
        self.urls = [website]
        self.links = [website]

    def run(self):
        for url in self.urls:
            r = Render(url)
            #for url in  
        
        #self.qwebframe.load(self.qurl)
    
    def quit(self):
        print 'finished'
        self.app.quit()

#if __name__ == '__main__':
    #url='http://www.baidu.com/'
    #r = Render(url)
    #del r
urls = [
        'http://stackoverflow.com',
        'http://github.com',
        'http://bitbucket.org',
        'http://news.ycombinator.com',
        'http://slashdot.org',
        'http://www.reddit.com',
        'http://www.dzone.com',
        'http://www.ideone.com',
        'http://jsfiddle.net',
    ]

if __name__=='__main__':
    url = 'http://demo.aisec.cn/demo/aisec/'
    app = QApplication(sys.argv)
    r = Render(url)
    print r.urls
    #app.exec_()
    app.quit()
    #del r
    #$print r.urls
