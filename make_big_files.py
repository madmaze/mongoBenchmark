#! /usr/bin/env python

import os
import argparse

parser = argparse.ArgumentParser(description="Takes the files in a directory and concatenates them (n) at a time")
parser.add_argument('--data-dir', type=str, dest='data_dir', default='/home/ubuntu/s3/', help='the directory containing data to load into the db')
parser.add_argument('--chunk-size', type=int, dest='chunk_size', default=200, help='the number of s3 files to concatenate into one file.')
parser.add_argument('--output', type=str, dest='output', default='/mnt/big_chunks/', help='the directory to place output files in')

args = parser.parse_args()

file_list = os.listdir(args.data_dir)
total_count = len(file_list)
partitions = [ file_list[args.chunk_size * i : args.chunk_size * (i + 1)] for i in xrange(total_count / args.chunk_size)]

for idx, file_list in enumerate(partitions):
	output_file = open(args.output + str(idx), 'w')
	for input_path in file_list:
		input_file = open(args.data_dir + '/' + input_path)
		data = input_file.read()
		input_file.close()
		output_file.write(data)
	output_file.close()
	print 'wrote file',idx

