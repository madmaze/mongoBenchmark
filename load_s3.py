#! /usr/bin/env python

import pymongo
import gridfs
import os
import argparse

parser = argparse.ArgumentParser(description="Throw a section of the S3 bucket at a mongo server")
parser.add_argument('--node-count', type=int, dest='node_count', action='store', required=True, help='the number of nodes throwing data at mongo')
parser.add_argument('--node', type=int, dest='node', action='store', required=True, help='the id of this node, starting from 0')
parser.add_argument('--user', type=str, dest='user', action='store', help='the mongodb user')
parser.add_argument('--passwd', type=str, dest='passwd', action='store', help='the mongodb password')
parser.add_argument('--server', type=str, dest='server', action='store', help='the mongo server')
parser.add_argument('--port', type=str, dest='port', action='store', help='the mongodb port')

args = parser.parse_args()
print 'node count: ', args.node_count
print 'node id: ', args.node
exit(0)

max_id = 30
my_id = 0
base_dir = '/home/ubuntu/s3/'
file_list = os.listdir(base_dir)
total_count = len(file_list)
chunk_size = total_count / max_id
# Take care of the last few files at the end
file_list = file_list[chunk_size * my_id : chunk_size * (my_id+1)]

connection = pymongo.Connection('mongodb://dba:sql@ds037637-a.mongolab.com:37637/mongotest')
#connection = pymongo.Connection('mongodb://admin:adminpw@23.20.124.206:27017/testdb')
db = connection['mongotest']
#db = connection['testdb']

grid = gridfs.GridFS(db, 'brains')

i = 0
for path in file_list:
	f = open(base_dir + path)
	data = f.read()
	grid.put(data, filename=path)
	i += 1
	if i >= 1000:
		break
