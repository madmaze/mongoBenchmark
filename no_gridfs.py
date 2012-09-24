#! /usr/bin/env python

import pymongo
import os
import argparse
import time

parser = argparse.ArgumentParser(description="Throw a section of the S3 bucket at a mongo server")
parser.add_argument('--node-count', type=int, dest='node_count', action='store', required=True, help='the number of nodes throwing data at mongo')
parser.add_argument('--node', type=int, dest='node', action='store', required=True, help='the id of this node, starting from 0')
parser.add_argument('--user', type=str, dest='user', action='store', default='testusr', help='the mongodb user')
parser.add_argument('--passwd', type=str, dest='passwd', action='store', default='testpw', help='the mongodb password')
parser.add_argument('--server', type=str, dest='server', action='store', default='mongoServ1', help='the mongo server')
parser.add_argument('--port', type=str, dest='port', action='store', default='27017', help='the mongodb port')
parser.add_argument('--db', type=str, dest='db', action='store', default='testdb', help='the database name')
parser.add_argument('--data-dir', type=str, dest='data_dir', default='/home/ubuntu/s3/', help='the directory containing data to load into the db')
parser.add_argument('--collection', type=str, dest='collection', default='brains', help='the mongo collection to use')
# TODO make sure that this default is higher than the number of files from S3
parser.add_argument('--limit-files', type=int, dest='limit_files', default=100000, help='limit the number of files to throw at the mongo server')
parser.add_argument('--enable-checkpoint', dest='enable_checkpoint', action='store_const', const=True, default=False, help='wait for the other client nodes to load data into memory before assaulting mongodb')
parser.add_argument('--enable-prompt', dest='enable_prompt', action='store_const', const=True, default=False, help='prompt for input after loading from disk and before assaulting the server')

args = parser.parse_args()

file_list = os.listdir(args.data_dir)
total_count = len(file_list)
chunk_size = total_count / args.node_count
# Take care of the last few files at the end
chunk_size = min(chunk_size, args.limit_files)
file_list = file_list[chunk_size * args.node : chunk_size * (args.node + 1)]

#connection = pymongo.Connection('mongodb://dba:sql@ds037637-a.mongolab.com:37637/mongotest')
#connection = pymongo.Connection('mongodb://testuser:testpw@23.20.124.206:27017/testdb')
connection = pymongo.Connection('mongodb://' + args.user + ':' + args.passwd + '@' + args.server + ':' + args.port + '/' + args.db)
#db = connection['mongotest']
db = connection[args.db]
collection = db[args.collection]

in_memory_files ={}
documents = []
for path in file_list:
	f = open(args.data_dir + '/' + path)
	data = f.read()
	f.close()
	in_memory_files[path] = data
	documents.append({'filename':path, 'data':data})

print 'All files for node',args.node,'are loaded into memory.'

if args.enable_checkpoint:
	f = open('node_' + str(args.node), 'w')
	f.close()

try:
	# TODO Rich says to use inotify
	if args.enable_checkpoint:
		for i in xrange(args.node_count):
			while not os.path.exists('node_'+str(i)):
				pass
	if args.enable_prompt:
		raw_input('Press enter to continue.')
	
	start = time.time()
	for doc in documents:
		collection.insert(doc)
	#collection.insert(documents)
	end = time.time()
	deltaTime = end - start
	print chunk_size,'files in', deltaTime,'seconds'
	print chunk_size / deltaTime, 'files / second'
finally:
	if args.enable_checkpoint:
		try:
			os.remove('node_' + str(args.node))
		except:
			pass
