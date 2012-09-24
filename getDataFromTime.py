#! /usr/bin/env python

import csv
import re
import sys
import argparse
import datetime

parser = argparse.ArgumentParser()
parser.add_argument('input_path', type=str, action='store')
parser.add_argument('--start-time', type=str, dest='start_time', action='store', required=True)
parser.add_argument('--length', type=int, dest='length', action='store', required=True)
parser.add_argument('--output', type=str, dest='output', action='store')

args = parser.parse_args()

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

start_time = string_to_datetime(args.start_time)
end_time = start_time + datetime.timedelta(seconds=args.length)

if args.output == None:
	output_file = sys.stdout
else:
	output_file = open(args.output, 'wb')
writer = csv.writer(output_file, delimiter=',', quotechar='"')

input_file = open(args.input_path, 'rb')
reader = csv.reader(input_file, delimiter=',', quotechar='"')
for row in reader:
	if len(row) == 0:
		continue
	if re.match(datetime_regex, row[0]) != None:
		cur_date = string_to_datetime(row[0])
		if cur_date >= start_time and cur_date <= end_time:
			writer.writerow(row)
