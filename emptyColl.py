#! /usr/bin/env python

import pymongo
import sys
import timeit

user = "testusr"
passwd = "testpw"
dbname = "testdb"
collect = "test2"
server = "mongoServ1:27017"
inserts = 1
execcnt = 1
id = 1

startme = """
import pymongo
conn = pymongo.Connection('mongodb://%s:%s@%s/%s')

db = conn['%s']
col = db.collection
inserts = %d
id = %d""" % (user,passwd,server,dbname,collect,inserts,id) 

timecode = """ 
col.remove({})
print col.count()
#	if not (col.find_one(str(id) + str(x)) == x):
#	  print "Retrieve of %d on %s failed: got %s" % (x,id,col.find_one(str(id) + str(x)))"""

runme = timeit.Timer(stmt=timecode,setup=startme)

res = runme.timeit(number=execcnt)

