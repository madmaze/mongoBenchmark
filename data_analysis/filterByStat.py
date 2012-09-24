#! /usr/bin/env python

import csv
import re
import sys
import argparse
import datetime

parser = argparse.ArgumentParser()
parser.add_argument('input_files', nargs='+', type=str, help='the files to take as input')
parser.add_argument('--type', type=str, dest='type', action='store', required=True)
parser.add_argument('--ouput', type=str, dest='output', action='store')

args = parser.parse_args()

inputs = [ open(name, 'rb') for name in args.input_files ]

if args.output == None:
	output_file = sys.stdout
else:
	output_file = open(args.output, 'wb')
writer = csv.writer(output_file, delimiter=',', quotechar='"')

time_buckets = {}

datetime_regex = re.compile(r'(?P<day>\d\d)-(?P<month>\d\d) (?P<hours>\d\d?)\:(?P<minutes>\d\d)\:(?P<seconds>\d\d)')
time_regex = re.compile(r'(?P<hours>\d\d?)\:(?P<minutes>\d\d)\:(?P<seconds>\d\d)')

def string_to_datetime(date_str):
	m = re.match(datetime_regex, date_str)
	today = datetime.datetime.today()
	if m != None:
		d = m.groupdict()
		return datetime.datetime(today.year, int(d['month']), int(d['day']), int(d['hours']), int(d['minutes']), int(d['seconds']))
	m = re.match(time_regex, date_str)
	if m != None:
		d = m.groupdict()
		return datetime.datetime(today.year, today.month, today.day, int(d['hours']), int(d['minutes']), int(d['seconds']))
	else:
		return None
#TODO take the right ranges
if args.type == 'cpu':
	start_col = 1
	end_col = 5
elif args.type == 'disk':
	start_col = 7
	end_col = 9

for cur_file in inputs:
	cur_reader = csv.reader(cur_file)
	for row in cur_reader:
		if len(row) == 0:
			continue
		if re.match(datetime_regex, row[0]):
			cur_time = string_to_datetime(row[0])
			if cur_time not in time_buckets:
				time_buckets[cur_time] = []
			time_buckets[cur_time] += row[start_col:end_col]

sorted_keys = time_buckets.keys()
sorted_keys.sort()
for key in sorted_keys:
	writer.writerow([key] + time_buckets[key])
