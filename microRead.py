#! /usr/bin/env python

import pymongo
import sys
import timeit

user = "testusr"
passwd = "testpw"
dbname = "testdb"
#server = "ds037627-a.mongolab.com:37627"
server = "mongoServ1:27017"
inserts = 1
execcnt = 1
id = 1
#try:
#  id = int(sys.argv[1])
#except:
#  print "You forgot to give me an ID"
#  sys.exit(-1)
#if len(sys.argv) > 2 and int(sys.argv[2]):
#  inserts = int(sys.argv[2])

startme = """
import pymongo
conn = pymongo.Connection('mongodb://%s:%s@%s/%s')

db = conn['mongodb']
col = db.collection
inserts = %d
id = %d""" % (user,passwd,server,dbname,inserts,id) 

timecode = """ 
for x in range(0,inserts):
        print col.find_one()
#        print col.count()
#	if not (col.find_one(str(id) + str(x)) == x):
#	  print "Retrieve of %d on %s failed: got %s" % (x,id,col.find_one(str(id) + str(x)))"""

runme = timeit.Timer(stmt=timecode,setup=startme)

res = runme.timeit(number=execcnt)

print "Successfully tried %d retrieves in %f seconds" % (inserts * execcnt,res)
