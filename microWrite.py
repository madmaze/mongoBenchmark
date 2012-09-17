#! /usr/bin/env python

import pymongo
import sys

user = "user"
passwd = "whatever"
server = "ds037627-a.mongolab.com:37627"
inserts = 50
id = 1
try:
  id = int(sys.argv[1])
except:
  print "You forgot to give me an ID"
  sys.exit(-1)
if len(sys.argv) > 2 and int(sys.argv[2]):
  inserts = int(sys.argv[2])

conn = pymongo.Connection('mongodb://%s:%s@%s/mongodb' % (user,passwd,server))

db = conn['mongodb']
col = db.collection

for x in range(0,inserts):
	col.insert({str(x):str(x)}, safe = True)
print "Successfully tried %d inserts" % inserts