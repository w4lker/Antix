#/usr/bin/python27
#coding:utf-8

import MySQLdb

class SqlOperator:
    
    _conn = None
    _cur = None
    
    def connect(self,dbconfig):
        try:
            self._conn = MySQLdb.connect(host=dbconfig['host'],port=dbconfig['port'],user=dbconfig['user'],passwd=dbconfig['passwd'],db=dbconfig['db'],charset=dbconfig['charset'])
        except MySQLdb.Error,e:
            print "Mysql Error %d:%s" % (e.args[0],e.args[1])
            return False
        self._cur = self._conn.cursor()
        print "连接成功!"
    
    def close(self):  
        self._cur.close()
        self._conn.close()
    
    def query(self,sql):
        try:
            result = self._cur.excute(sql)
        except MySQLdb.Error,e:
            print "Mysql Error %d:%s" % (e.args[0],e.args[1])
            result = False
        return result
    
    def modify(self,sql):
        try:
            result = self._cur.excute(sql)
            self._cur.commit()
        except MySQLdb.Error,e:
            print "Mysql Error %d:%s" % (e.args[0],e.args[1])
            result = False
        return result
    
    
        
    
    