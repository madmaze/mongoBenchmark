#! /usr/bin/env python

import os
import argparse
import base64

parser = argparse.ArgumentParser(description="Base64 encode all the files in a directory")
parser.add_argument('--data-dir', type=str, dest='data_dir', default='/home/ubuntu/s3/', help='the directory containing data to load into the db')
parser.add_argument('--output', type=str, dest='output', default='/mnt/b64/', help='the directory to place output files in')

args = parser.parse_args()

file_list = os.listdir(args.data_dir)

for path in file_list:
	print 'starting', path
	in_file = open(os.path.join(args.data_dir, path))
	data = in_file.read()
	in_file.close()
	output = open(os.path.join(args.output, path), 'w')
	output.write(base64.b64encode(data))
	output.close()

