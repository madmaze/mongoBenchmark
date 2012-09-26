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
user = []
system = []
idle = []
waiting = []

for row in reader:
	if len(row) == 0:
		continue
	if is_datetime(row[0]):
		times.append(string_to_datetime(row[0]))
		user.append(float(row[1]))
		system.append(float(row[2]))
		idle.append(float(row[3]))
		waiting.append(float(row[4]))

del reader

first_time = times[0]
delta_times = [ (time - first_time).seconds for time in times]
user_sys = [ user[i] + system[i] for i in xrange(len(user)) ]
usw = [user_sys[i] + waiting[i] for i in xrange(len(user)) ]

fig = pyplot.figure()
ax = fig.add_subplot(1, 1, 1)
ax.fill_between(delta_times, 0, user, facecolor='#FF0000')
ax.fill_between(delta_times, user, user_sys, facecolor='#00FF00')
ax.fill_between(delta_times, user_sys, usw, facecolor='#5555FF')
ax.set_ylabel('CPU Utilization (%)')
ax.set_xlabel('Time (s)')

pyplot.show()
