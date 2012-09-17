#! /usr/bin/env python

import pymongo
import sys
import timeit


user = "testusr"
passwd = "testpw"
dbname = "testdb"
#server = "ds037627-a.mongolab.com:37627"
server = "mongoServ1:27017"
inserts = 5000
execcnt = 500
collname = "collection"
id = 1
try:
  id = int(sys.argv[1])
except:
  print "You forgot to give me an ID"
  sys.exit(-1)
#if len(sys.argv) > 2 and int(sys.argv[2]):
#  inserts = int(sys.argv[2])

startme = """
import pymongo
import hashlib
conn = pymongo.Connection('mongodb://%s:%s@%s/%s')

db = conn['%s']
col = db.%s
inserts = %d
id = %d
pre = 0""" % (user,passwd,server,dbname,dbname,collname,inserts,id) 

timecode = """
for x in range(0,inserts):
	try:
	  #hashval = hashlib.sha1()
#	  hashval.update(str(x))
	  col.insert({str(pre) + str(id) + str(x):str(x)}, safe = False)
        except:
          print "Oops I bombed out"
          import traceback
          traceback.print_exc()
pre += 1 """

runme = timeit.Timer(stmt=timecode,setup=startme)

res = runme.timeit(number=execcnt)

print "Successfully tried %d inserts in %f seconds" % (inserts * execcnt,res)
