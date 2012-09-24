#! /usr/bin/env python

import pymongo
import sys
import timeit


user = "testusr"
passwd = "testpw"
dbname = "testdb"
#server = "ds037627-a.mongolab.com:37627"
server = "localhost:27017"
inserts = 5000
execcnt = 500
collname = "collection"

startme = """
import pymongo
import hashlib
conn = pymongo.Connection('mongodb://%s:%s@%s/%s')

db = conn['%s']
col = db.%s
inserts = %d
""" % (user,passwd,server,dbname,dbname,collname,inserts)

timecode = """
for x in range(0,inserts):
	try:
	  #hashval = hashlib.sha1()
#	  hashval.update(str(x))
	  col.insert({}, safe = False)
        except:
          print "Oops I bombed out"
          import traceback
          traceback.print_exc()
"""

runme = timeit.Timer(stmt=timecode,setup=startme)

res = runme.timeit(number=execcnt)

print "Successfully tried %d inserts in %f seconds" % (inserts * execcnt,res)
