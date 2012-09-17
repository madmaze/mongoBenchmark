#! /usr/bin/env python

import pymongo
import sys
import timeit

user = "user"
passwd = "whatever"
server = "ds037627-a.mongolab.com:37627"
inserts = 50
execcnt = 500
id = 1
try:
  id = int(sys.argv[1])
except:
  print "You forgot to give me an ID"
  sys.exit(-1)
if len(sys.argv) > 2 and int(sys.argv[2]):
  inserts = int(sys.argv[2])

startme = """
import pymongo
conn = pymongo.Connection('mongodb://%s:%s@%s/mongodb')

db = conn['mongodb']
col = db.collection
inserts = %d""" % (user,passwd,server,inserts) 

timecode = """ 
for x in range(0,inserts):
	col.insert({str(x):str(x)}, safe = True)"""

runme = timeit.Timer(stmt=timecode,setup=startme)

res = runme.timeit(number=execcnt)

print "Successfully tried %d inserts in %f seconds" % (inserts * execcnt,res)
