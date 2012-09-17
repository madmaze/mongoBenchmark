#! /usr/bin/env python

import pymongo
import gridfs
import os
import argparse
import time

parser = argparse.ArgumentParser(description="Throw a section of the S3 bucket at a mongo server")
parser.add_argument('--node-count', type=int, dest='node_count', action='store', required=True, help='the number of nodes throwing data at mongo')
parser.add_argument('--node', type=int, dest='node', action='store', required=True, help='the id of this node, starting from 0')
parser.add_argument('--user', type=str, dest='user', action='store', default='testuser', help='the mongodb user')
parser.add_argument('--passwd', type=str, dest='passwd', action='store', default='testpw', help='the mongodb password')
parser.add_argument('--server', type=str, dest='server', action='store', default='mongoServ1', help='the mongo server')
parser.add_argument('--port', type=str, dest='port', action='store', default='27017', help='the mongodb port')
parser.add_argument('--db', type=str, dest='db', action='store', default='testdb', help='the database name')
parser.add_argument('--data-dir', type=str, dest='data_dir', default='/home/ubuntu/s3/', help='the directory containing data to load into the db')
parser.add_argument('--collection', type=str, dest='collection', default='brains', help='the mongo collection to use')
# TODO make sure that this default is higher than the number of files from S3
parser.add_argument('--limit-files', type=int, dest='limit_files', default=100000, help='limit the number of files to throw at the mongo server')

args = parser.parse_args()

file_list = os.listdir(args.data_dir)
total_count = len(file_list)
chunk_size = total_count / args.node_count
# Take care of the last few files at the end
file_list = file_list[chunk_size * args.node : chunk_size * (args.node + 1)]

#connection = pymongo.Connection('mongodb://dba:sql@ds037637-a.mongolab.com:37637/mongotest')
#connection = pymongo.Connection('mongodb://testuser:testpw@23.20.124.206:27017/testdb')
connection = pymongo.Connection('mongodb://' + args.user + ':' + args.passwd + '@' + args.server + ':' + args.port + '/' + args.db)
#db = connection['mongotest']
db = connection[args.db]

grid = gridfs.GridFS(db, args.collection)

in_memory_files ={}
i = 0
for path in file_list:
	f = open(args.data_dir + path)
	data = f.read()
	f.close()
	in_memory_files[path] = data
	i += 1
	if i >= args.limit_files:
		break;
f = open('node_' + str(args.node), 'w')
f.close()
try:
	for i in xrange(args.node_count):
		while not os.path.exists('node_'+str(i)):
			pass
	
	start = time.time()
	for (path, data) in in_memory_files.iteritems():
		grid.put(data, filename=path)
	end = time.time()
	deltaTime = end - start
	print len(in_memory_files),'files in', deltaTime,'seconds'
	print len(in_memory_files) / deltaTime, 'files / second'
finally:
	try:
		os.remove('node_' + str(args.node))
	except:
		pass
