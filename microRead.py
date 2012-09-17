#! /usr/bin/env python

import pymongo
import sys

user = "user"
passwd = "whatever"
server = "ds037627-a.mongolab.com:37627"
inserts = 50
if sys.argc > 1 and int(sys.argv[1]):
  inserts = int(sys.argv[1])

conn = pymongo.Connection('mongodb://%s:%s@%s/mongodb' % (user,passwd,server))

db = conn['mongodb']
col = db.collection

for x in range(0,inserts):
	col.insert({str(x):str(x)}, safe = True)
print "Successfully tried %d inserts" % inserts