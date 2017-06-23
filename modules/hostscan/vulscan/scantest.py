# coding:utf-8
import urllib2
import thread
import time
import pymongo
import sys
import datetime
import hashlib
import json
import re
import uuid
import os
from VulScan import *

sys.path.append(sys.path[0] + '/vuldb')
sys.path.append(sys.path[0] + "/../")
from Config import ProductionConfig

db_conn = pymongo.MongoClient(ProductionConfig.DB, ProductionConfig.PORT)
na_db = getattr(db_conn, ProductionConfig.DBNAME)
na_db.authenticate(ProductionConfig.DBUSERNAME, ProductionConfig.DBPASSWORD)
na_task = na_db.Task
na_result = na_db.Result
na_plugin = na_db.Plugin
na_config = na_db.Config
na_heart = na_db.Heartbeat
lock = thread.allocate()
PASSWORD_DIC = []
THREAD_COUNT = 50
TIMEOUT = 10
PLUGIN_DB = {}
TASK_DATE_DIC = {}
WHITE_LIST = []

if __name__ == '__main__':
    init()
    PASSWORD_DIC, THREAD_COUNT, TIMEOUT, WHITE_LIST = get_config()
    thread.start_new_thread(monitor, ())
    while True:
        task_id, task_plan, task_target, task_plugin = queue_get()   #设置task_target即可扫描
#        if task_id == '':
#            time.sleep(10)
#            continue
        PLUGIN_DB = {}  # 清理插件缓存
        for task_netloc in task_target:
            while True:
                if int(thread._count()) < THREAD_COUNT:
                    if task_netloc[0] in WHITE_LIST: break
                    thread.start_new_thread(vulscan, (task_id, task_netloc, task_plugin))
                    break
                else:
                    time.sleep(2)
        if task_plan == 0: na_task.update({"_id": task_id}, {"$set": {"status": 2}})
