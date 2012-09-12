#! /usr/bin/env python

import pymongo
import gridfs
import os

base_dir = '/home/ubuntu/s3/'
file_list = os.listdir(base_dir)

connection = pymongo.Connection('mongodb://dba:sql@ds037637-a.mongolab.com:37637/mongotest')
db = connection['mongotest']

grid = gridfs.GridFS(db, 'brains')

i = 0
for path in file_list:
	f = open(base_dir + path)
	data = f.read()
	grid.put(data, filename=path)
	i += 1
	if i >= 1000:
		break
