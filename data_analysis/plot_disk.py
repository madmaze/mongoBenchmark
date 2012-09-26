#! /usr/bin/env python

import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument('input_file', nargs='?', type=argparse.FileType('r'), default=sys.stdin)

args = parser.parse_args()

import matplotlib.pyplot as pyplot
import csv
import datetime
from util import string_to_datetime, is_datetime

reader = csv.reader(args.input_file)

times = []
read = []
write = []

for row in reader:
	if len(row) == 0:
		continue
	if is_datetime(row[0]):
		times.append(string_to_datetime(row[0]))
		read.append(float(row[1]))
		write.append(float(row[2]))

del reader

first_time = times[0]
delta_times = [ (time - first_time).seconds for time in times]

fig = pyplot.figure()
ax = fig.add_subplot(1, 1, 1)
ax.plot(delta_times, read, color='#5555FF', linewidth=2)
ax.plot(delta_times, write, color='#00FF00', linewidth=2)
ax.set_ylabel('Disk Activity')
ax.set_xlabel('Time (s)')

pyplot.show()
