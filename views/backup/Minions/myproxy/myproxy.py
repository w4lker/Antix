#!/usr/bin/env python
#coding:utf-8
"""
This example builds on mitmproxy's base proxying infrastructure to
implement functionality similar to the "sticky cookies" option.

Heads Up: In the majority of cases, you want to use inline scripts.
"""
import os
import string
import sys
import urlparse
import traceback
from libmproxy import controller, proxy
from libmproxy.proxy.server import ProxyServer
from libs.db import database
from libs.flowhandle import *
from libs.vulscan import Vulscan
import threading
import time
import base64
import magic


class StickyMaster(controller.Master):

    def __init__(self, server,proxy_enabled,negative_type,target):
        controller.Master.__init__(self, server)
        self.stickyhosts = {}
        self.proxy_enabled = proxy_enabled
        self.negative_type = negative_type
        self.target = target

        
    def run(self):
        try:
            return controller.Master.run(self)
        except KeyboardInterrupt:
            self.shutdown()

    def handle_request(self, flow):
        hid = (flow.request.host, flow.request.port)
        if "cookie" in flow.request.headers:
            self.stickyhosts[hid] = flow.request.headers.get_all("cookie")
        elif hid in self.stickyhosts:
            flow.request.headers.set_all("cookie", self.stickyhosts[hid])
        flow.reply()

    def handle_response(self, flow):
        print flow.request.url
        hid = (flow.request.host, flow.request.port)
        if "set-cookie" in flow.response.headers:
            self.stickyhosts[hid] = flow.response.headers.get_all("set-cookie")
        flow.reply()
        
        try:
            if self.target == '' or flow.request.host in self.target.split(';'):
                if 'content-type' in flow.response.headers:
                    content_type = flow.response.headers['content-type'].split(';')[0] 
                else:
                    m = magic.Magic(magic_file=r'C:\python27\magicfile\magic',mime=True)
                    content_type = m.from_buffer(flow.response.body)
                
                file_type = urlparse.urlparse(flow.request.url)[2].split('.')[-1].lower()
                
                if content_type != 'text/html' or file_type in self.negative_type:
                    print 'negative content-type!'
                
                else:
                    v = Vulscan(flow)                  #调用扫描类，进行扫描，测试网站http://www.tjwfn.com/net_list.jsp?ieb12eki&zxlb=1
                    v.start()                    
                    if self.proxy_enabled == 'true':
                        req = get_raw_req(flow)
                        rsp = get_raw_rsp(flow)
                        db = database()
                        cur = db.connectdb('./db.sqlite3')
                        t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                        sqlcmd = '''insert into minions_proxydata(status_code,method,host,url,request,response,time)values(%d,'%s','%s','%s','%s','%s','%s')''' % (flow.response.status_code,flow.request.method,flow.request.host,flow.request.url,req,rsp,t)
                        db.modify(cur,sqlcmd)    
                        db.closedb(cur)   
                
        except Exception as e:
            db = database()
            cur = db.connectdb('./db.sqlite3')   
            tb = traceback.format_exc().replace("'","''")
            message = e.message
            sqlcmd = '''insert into minions_sysexceptions(traceback,errmessage,time)values('%s','%s','%s')''' % (tb,message,time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
            db.modify(cur,sqlcmd)
            db.closedb(cur)
        
                       