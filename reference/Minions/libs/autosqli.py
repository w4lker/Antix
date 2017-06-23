#!/usr/bin/python
#-*-coding:utf-8-*-
import requests
import time
import json
from libmproxy import flow
from db import database
from flowhandle import * 


class AutoSqli(object):

    """
    使用sqlmapapi的方法进行与sqlmapapi建立的server进行交互
    By Manning
    """

    def __init__(self, server='', scan_flow ='',level=1,risk=1,proxy=None):
        super(AutoSqli, self).__init__()
        self.server = server
        if self.server[-1] != '/':
            self.server = self.server + '/'
        self.scan_flow = scan_flow
        self.target = scan_flow.request.url
        self.taskid = ''
        self.engineid = ''
        self.status = ''
        self.headers = dict(scan_flow.request.headers)
        self.data = scan_flow.request.body
        #self.referer = scan_flow.request.headers['referer']
        if 'cookie' in scan_flow.request.headers:
            self.cookie = scan_flow.request.headers['cookie']
        else:
            self.cookie = ''
        self.start_time = time.time()
        self.db = database()
        self.cur = self.db.connectdb('./db.sqlite3')
        self.level = level
        self.risk = risk
        self.proxy = proxy

    def task_new(self):
        self.taskid = json.loads(
            requests.get(self.server + 'task/new').text)['taskid']
        print 'Created new task: ' + self.taskid
        if len(self.taskid) > 0:
            return True
        return False

    def task_delete(self):
        if json.loads(requests.get(self.server + 'task/' + self.taskid + '/delete').text)['success']:
            print '[%s] Deleted task' % (self.taskid)
            return True
        return False

    def scan_start(self):
        headers = {'Content-Type': 'application/json'}
        payload = self.scan_payload()
        url = self.server + 'scan/' + self.taskid + '/start'
        t = json.loads(
            requests.post(url, data=json.dumps(payload), headers=headers).text)
        self.engineid = t['engineid']
        if len(str(self.engineid)) > 0 and t['success']:
            t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            sqlcmd = '''insert into minions_sqliscan (taskid,url,request,time,status)values('%s','%s','%s','%s','%s')''' % (self.taskid,self.target,get_raw_req(self.scan_flow),t,'running')
            self.db.modify(self.cur,sqlcmd)
            print 'Started scan'
            return True
        return False
    
    def scan_payload(self):
        payload = {
                  'url': self.target,
                  'data': self.data,
                  'level': int(self.level),
                  'risk': int(self.risk),
                  'cookie': self.cookie,
                  'proxy': self.proxy
               }
        return payload

    def scan_status(self):
        self.status = json.loads(
            requests.get(self.server + 'scan/' + self.taskid + '/status').text)['status']
        if self.status == 'running':
            return 'running'
        elif self.status == 'terminated':
            return 'terminated'
        else:
            return 'error'

    def scan_data(self):
        self.data = json.loads(
            requests.get(self.server + 'scan/' + self.taskid + '/data').text)['data']
        if self.status == 'terminated':
            if len(self.data) == 0:
                sqlcmd = '''delete from minions_sqliscan where taskid = '%s' ''' % self.taskid 
                self.db.modify(self.cur,sqlcmd)
                print 'not injected:\t'
            else:
                sqlcmd = '''update minions_sqliscan set status = 'injected' where taskid = '%s'  ''' % self.taskid
                self.db.modify(self.cur,sqlcmd)
                print 'injected:\t' + self.target
        
        elif self.status == 'timeout':
            sqlcmd = '''update minions_sqliscan set status = 'timeout' where taskid = '%s'  ''' % self.taskid
            self.db.modify(self.cur,sqlcmd) 
        
        else:
            sqlcmd = '''update minions_sqliscan set status = 'error' where taskid = '%s'  ''' % self.taskid
            self.db.modify(self.cur,sqlcmd)              

    def option_set(self):
        headers = {'Content-Type': 'application/json'}
        option = {"options": {
                    'smart':True,
                    }
                 }
        url = self.server + 'option/' + self.taskid + '/set'
        t = json.loads(
            requests.post(url, data=json.dumps(option), headers=headers).text)
        print t

    def scan_stop(self):
        json.loads(
            requests.get(self.server + 'scan/' + self.taskid + '/stop').text)['success']

    def scan_kill(self):
        json.loads(
            requests.get(self.server + 'scan/' + self.taskid + '/kill').text)['success']

    def run(self):
        if not self.task_new():
            return False
        self.option_set()
        if not self.scan_start():
            return False
        while True:
            if self.scan_status() == 'running':
                time.sleep(10)
            elif self.scan_status() == 'terminated':
                break
            else:
                break
            print time.time() - self.start_time
            if time.time() - self.start_time > 3000:
                error = True
                self.status = 'timeout'
                self.scan_stop()
                self.scan_kill()
                break
        self.scan_data()
        self.task_delete()
        print time.time() - self.start_time
    
    #def time_out(self):
     #   if time.time() - self.start_time > 3000:   #超时时间后续可从数据库中读取，web平台中设置