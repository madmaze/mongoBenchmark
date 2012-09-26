#! /usr/bin/env python

import csv
import re
import sys
import argparse
import datetime
from util import string_to_datetime, is_datetime

parser = argparse.ArgumentParser()
parser.add_argument('input_file', type=argparse.FileType('r'), action='store')
parser.add_argument('--start-time', type=str, dest='start_time', action='store', required=True)
parser.add_argument('--length', type=int, dest='length', action='store', required=True)
parser.add_argument('--output', nargs='?', type=argparse.FileType('w'), default=sys.stdout, dest='output', action='store')

args = parser.parse_args()

start_time = string_to_datetime(args.start_time)
end_time = start_time + datetime.timedelta(seconds=args.length)

writer = csv.writer(args.output, delimiter=',', quotechar='"')

reader = csv.reader(args.input_file, delimiter=',', quotechar='"')
for row in reader:
	if len(row) == 0:
		continue
	if row[0] in ['system', 'time', 'Host:']:
		writer.writerow(row)
	elif is_datetime(row[0]):
		cur_date = string_to_datetime(row[0])
		if cur_date >= start_time and cur_date <= end_time:
			writer.writerow(row)
