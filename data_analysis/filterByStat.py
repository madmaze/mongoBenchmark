#! /usr/bin/env python

import csv
import re
import sys
import argparse
import datetime
from util import string_to_datetime, is_datetime

parser = argparse.ArgumentParser()
parser.add_argument('input_files', nargs='*', type=argparse.FileType('r'), default=[sys.stdin], help='the files to take as input')
parser.add_argument('--type', type=str, dest='type', action='store', required=True)
parser.add_argument('--output', nargs='?', type=argparse.FileType('w'), default=sys.stdout, dest='output', action='store')

args = parser.parse_args()

writer = csv.writer(args.output, delimiter=',', quotechar='"')

time_buckets = {}

#TODO take the right ranges
if args.type == 'cpu':
	desired_col_names = ['usr','sys','idl','wai']
elif args.type == 'disk':
	desired_col_names = ['read', 'writ']
elif args.type == 'net':
	desired_col_names = ['recv', 'send']

host_list = []

for cur_file in args.input_files:
	cur_reader = csv.reader(cur_file)
	got_hostname = False
	# Get the indicies of the columns we want
	for row in cur_reader:
		if len(row) == 0:
			continue
		if row[0] == 'time': #This row has the column headings!
			desired_col_idx = [ row.index(col_name) for col_name in desired_col_names ]
			break
		elif (not got_hostname) and row[0] == 'Host:': # This row tells us which computer this is
			host_list.append(row[1])
			got_hostname = True
	
	# Read through the rest of the document and take out the data we want
	for row in cur_reader:
		if len(row) == 0:
			continue
		if is_datetime(row[0]):
			cur_time = string_to_datetime(row[0])
			if cur_time not in time_buckets:
				time_buckets[cur_time] = []
			time_buckets[cur_time] += [ row[idx] for idx in desired_col_idx ]

host_headings = ['Hosts']
for hostname in host_list:
	host_headings += [hostname] + [None]*(len(desired_col_names)-1)
writer.writerow(host_headings)

writer.writerow(['system time'] + desired_col_names * len(host_list))
sorted_keys = time_buckets.keys()
sorted_keys.sort()
for key in sorted_keys:
	writer.writerow([key] + time_buckets[key])
