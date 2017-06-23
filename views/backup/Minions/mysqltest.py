from libs.SqlOperator import SqlOperator

dbconfig = {'host':'10.18.100.105','port':3306,'user':'root','passwd':'fwb_PT2012','db':'autopenetration','charset':'gbk'}

db = SqlOperator()
db.connect(dbconfig)
db.close()