#coding:utf-8
#启动脚本，程序入口，负责启动代理和Django的web服务

import os
import string
from libmproxy import controller, proxy
from libmproxy.proxy.server import ProxyServer
from libs.db import *
from myproxy.myproxy import StickyMaster
from libs.flowhandle import *


db = database()
cur = db.connectdb('./db.sqlite3')
settings = dict(db.query(cur,'''select setting,value from minions_settings where module='proxy' '''))
db.closedb(cur)


c_d = os.path.expanduser("~/.mitmproxy/")

if settings['upstream_enabled'] == 'true':
    upstream_proxy = settings['upstream_proxy'].split(':')
    u_s = ['http',(upstream_proxy[0],int(upstream_proxy[1]))]
    config = proxy.ProxyConfig(mode='upstream',port=int(settings['port']),upstream_server=u_s,cadir=c_d)
else:
    config = proxy.ProxyConfig(port=int(settings['port']))
    
server = ProxyServer(config)
m = StickyMaster(server,proxy_enabled=settings['proxy_enabled'],negative_type=settings['negative_type'],target=settings['target'])
m.run()


