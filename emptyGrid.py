#! /usr/bin/env python

import pymongo
import sys
import timeit
import argparse
import time

parser = argparse.ArgumentParser(description="Throw a section of the S3 bucket at a mongo server")
#parser.add_argument('--node-count', type=int, dest='node_count', action='store', required=True, help='the number of nodes throwing data at mongo')
#parser.add_argument('--node', type=int, dest='node', action='store', required=True, help='the id of this node, starting from 0')
parser.add_argument('--user', type=str, dest='user', action='store', default='testusr', help='the mongodb user')
parser.add_argument('--passwd', type=str, dest='passwd', action='store', default='testpw', help='the mongodb password')
parser.add_argument('--server', type=str, dest='server', action='store', default='mongoServ1', help='the mongo server')
parser.add_argument('--port', type=str, dest='port', action='store', default='27017', help='the mongodb port')
parser.add_argument('--db', type=str, dest='db', action='store', default='testdb', help='the database name')
#parser.add_argument('--data-dir', type=str, dest='data_dir', default='/home/ubuntu/s3_a/', help='the directory containing data to dump from the db')
parser.add_argument('--collection', type=str, dest='collection', default='brains', help='the mongo collection to use')
# TODO make sure that this default is higher than the number of files from S3
#parser.add_argument('--limit-files', type=int, dest='limit_files', default=100000, help='limit the number of files to suck from the mongo server')
#parser.add_argument('--enable-checkpoint', dest='enable_checkpoint', action='store_const', const=True, default=False, help='wait for the other client nodes to load data into memory before assaulting mongodb')
parser.add_argument('--enable-prompt', dest='enable_prompt', action='store_const', const=True, default=False, help='prompt for input after loading from disk and before assaulting the server')

args = parser.parse_args()


startme = """
import pymongo
import gridfs
conn = pymongo.Connection('mongodb://%s:%s@%s/%s')

db = conn['%s']
col = db['%s']
""" % (args.user,args.passwd,args.server,args.db,args.db,args.collection) 

timecode = """
col.chunks.remove({})
col.files.remove({})
print "Emptied %s[%s] successfully"
""" % (args.db,args.collection)

runme = timeit.Timer(stmt=timecode,setup=startme)

res = runme.timeit(number=1)

