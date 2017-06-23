#!/usr/bin/python27
#coding:utf-8

import sqlite3
import string

class database:
    conn = None
    def connectdb(self,path):
        self.conn = sqlite3.connect(path,check_same_thread = False)
        if self.conn is not None:
            return self.conn.cursor()
        else:
            print "something wrong with database!"
            
    def closedb(self,cur):              
        if cur is not None:
            cur.close()
            self.conn.close()
            return True
          
          
    def query(self,cur,sql):
        if sql is not None and sql != '':
            cur.execute(sql)
            data = cur.fetchall()
            return data
        else:
            print "sqlCommand can not be null!"
   
    def  modify(self,cur,sql):
        try:
            if sql is not None and sql != '':
                cur.execute(sql)
                self.conn.commit()
            else:
                print "sqlCommand can not be null!"
        except Exception as e:
            print e.message
            
            
    def injectPrevention(param):
        return (param.replace("'",'')).replace('=','')
    