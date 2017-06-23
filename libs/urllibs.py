#!/usr/bin/python27
#coding:utf-8
import chardet
#import magic
import base64
#from libmproxy import flow
import os
#from db import database
import urlparse
from lxml import html

"""
def get_req_header(flow):
    return str(flow.request.headers)
"""

def get_raw_req(flow):
    """
    httpversion = "HTTP/" + str(flow.request.httpversion[0]) + '.' + str(flow.request.httpversion[1])
    req = flow.request.method +' ' + flow.request.url + ' ' + httpversion + '\n'
    for key,value in flow.request.headers:
        req += key + ':' +' ' + value + '\n'
    """
    headers = str(flow.request.headers)
    req = headers + '\n' + flow.request.body
    req = req.replace("'","''")
    return req

def get_raw_rsp(flow):
    headers = str(flow.response.headers)
    body = flow.response.body 
    
    db = database()
    cur = db.connectdb('./db.sqlite3')
    negative_type = db.query(cur,'''select value from minions_settings where setting='negative_type' ''')[0][0].split('|')
    
    """
    if flow.response.headers['content-type'] != []:
        content_type = flow.response.headers['content-type'].split(';')[0]       #如content-type存在，过滤content-type类型为css等
    else:
        m = magic.Magic(magic_file=r'C:\python27\magicfile\magic',mime=True)
        content_type = m.from_buffer(body)        
          
    if content_type in negative_type:
        body = base64.b64encode(body)
    else:
    
    if chardet.detect(body)['encoding']:
        encode_type = chardet.detect(body)['encoding']
        body = body.decode(encode_type,'replace') 
    """
    body = autodecode(body)
    rsp = headers + '\n' + body
    rsp = rsp.replace("'","''")
    return rsp

def autodecode(encode_str):
    if chardet.detect(encode_str)['encoding']:
        encode_type = chardet.detect(encode_str)['encoding']
        decode_str = encode_str.decode(encode_type,'replace')
        return decode_str
    return encode_str

def get_ext(url):
    return os.path.splitext(url)[1:]

def get_filename(url):
    return url.split('/')[-1]

def path_list(url):
    r = urlparse.urlsplit(str(url))
    path = r.path.split('/')
    tree = []
    
    for i in range(len(path)):
        node = {}
        if i == 0:
            u = r.scheme + '://' + r.netloc + '/' + path[i]
            node['id'] = u
            node['text'] = u
            node['parent'] = '#'
        elif i == len(path)-1:
            if path[i] == '':
                continue
            node['parent'] = u
            u = u.rstrip('/') + '/' + path[i]
            if r.query != '':
                u = u + '?' + r.query
                node['text'] = path[i] + '?' + r.query
            else:
                node['text'] = path[i]
            node['id'] = u
            
        else:
            node['parent'] = u
            u = u.rstrip('/') + '/' + path[i] + '/'
            node['id'] = u
            node['text'] = path[i]         
        tree.append(node)
    
    return tree

def get_atts(baseurl,strs,xpath):
    if type(strs) == 'str':
        print 'type not str'
    else:
        tree = html.fromstring(strs)
        tree.make_links_absolute(baseurl)
        atts = tree.xpath(xpath)
        return atts

def get_netloc(url):
    if urlparse.urlsplit(url).scheme == '':
        url = 'http://' + url
    return urlparse.urlsplit(url).scheme + '://' + urlparse.urlsplit(url).netloc
        
if __name__ == "__main__":
    url = 'http://www.123.com/1/2/3/test.php?a=1&b=2'
    print path_list(url)
    