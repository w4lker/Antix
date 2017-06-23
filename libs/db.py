#encoding:utf-8

from pymongo import MongoClient
import config

def conn():
    mngdb_uri = 'mongodb://' + config.db['uname'] + ':' + config.db['passwd'] + '@' + config.db['host'] + ':' + config.db['port'] + '/'
    client = MongoClient(mngdb_uri)
    db = client[config.db['db']]
    return db

def insert(post,**kwargs):
    db = conn()
    p = db.post[post]
    data = kwargs
    print data
    return p.insert(data)

def delete(post,**kwargs):
    db = conn()
    p = db.post[post]
    return p.remove(kwargs)

def update(post,db_filter,**kwargs):
    db = conn()
    p = db.post[post]
    return p.update(db_filter,{"$set":kwargs})

def select(post,*sort,**kwargs):   #查询条件如果大写表示升序，小写表示降序
    db = conn()
    p = db.post[post]
    if len(sort) != 0 :
        sort_list = sortFilter(sort)
        return p.find(kwargs).sort(sort_list)
    else:
        return p.find(kwargs)

def sortFilter(sort):
    sort_list = []
    for s in sort:
        if s.upper == s:
            sort_list.append((s,pymongo.ASCENDING))
        else:
            sort_list.append((s,pymongo.DESCENDING))
    return sort_list

if __name__ == '__main__':
    #insert('test',a=5,b=2,c=1)
    #delete('test',a=1,b=2,c=1)
    #update('test',{'c':1},b=123,a=123)
    select('test',a=3)
    

