#! /usr/bin/env python

import pymongo

conn = pymongo.Connection('mongodb://user:whatever@ds037627-a.mongolab.com:37627/mongodb')

db = conn['mongodb']
col = db.collection

for x in range(0,10):
	col.insert({str(x):str(x)}, safe = True)
print 'hoorayh'
