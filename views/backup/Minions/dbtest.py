#coding:utf-8
from libs.db import db

testdb = db()
cur = testdb.connectdb("./database/minions.db")
testdb.modify(cur,"create table 'manager'('id' INTEGER PRIMARY KEY autoincrement,'username' varhar(20) NOT NULL,'password' char(16) NOT NULL)")
testdb.modify(cur,"insert into manager(username,password) values('admin','e6e061838856bf47e1de730719fb2609')")