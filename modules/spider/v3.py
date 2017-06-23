import sys
#from WebPage import *
from PyQt4.Qt import *
from PyQt4.QtWebKit import *
 
class WebView(QWebView):
    def __init__(self):
	    super(WebView, self).__init__()
	    self.setPage(WebPage())
	    self.load(QUrl('http://www.qq.com'))
	    self.page().setLinkDelegationPolicy(QWebPage.DelegateAllLinks)
	    self.page().linkClicked.connect(self.linkClicked)
	    self.show()
 
    def linkClicked(self, url):
	    self.load(url)

	    import webbrowser
	    from PyQt4.QtWebKit import *
	
class WebPage(QWebPage):
    def __init__(self):
	super(WebPage, self).__init__()
	
    def acceptNavigationRequest(self, frame, request, type):
	if(type == QWebPage.NavigationTypeLinkClicked):
	    if(frame == self.mainFrame()):
		self.view().load(request.url())
	    else:
		webbrowser.open(request.url().toString())
		return False
	return QWebPage.acceptNavigationRequest(self, frame, request, type)
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    webView = WebView()
    sys.exit(app.exec_())