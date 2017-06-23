#coding:utf-8

from libs.xsscan.main import xsser
from libs.flowhandle import *
from libmproxy import flow
from netlib import odict

from urllib import urlencode

class XsserScan(object):
    def __init__(self,scan_flow = ''):
        self.flow = scan_flow
        """
        self.options['url'] = self.flow.request.url
        self.options['postdata']  = self.flow.request.body
        self.options['headers'] = get_req_header(self.flow)
        """
    
    def run(self):
        app = xsser()
        options = app.create_options()
        if isinstance(self.flow.request.query,odict.ODict):
            options.getdata = urlencode(self.flow.request.query)
        if self.flow.request.url.find('?') == -1:
            options.url = self.flow.request.url
        else:
            options.url = self.flow.request.url[:self.flow.request.url.find('?') + 1]
        options.fuzz = True
        options.heuristic = True
        options.threads = 20
        if self.flow.request.body != '':
            options.postdata = self.flow.request.body
        if "cookie" in self.flow.request.headers:
            options.cookie = self.flow.request.headers.get("cookie")
        if options.getdata == None and options.postdata == None:
            return
        if options:
            app.set_options(options)
            app.run()
            print app.heuris_test
            print app.taskid        
        app.land(True)

        

