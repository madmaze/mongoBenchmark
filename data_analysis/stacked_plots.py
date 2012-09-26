#! /usr/bin/env python

import csv
import re
import sys
import argparse
import datetime
from util import string_to_datetime, is_datetime
import subprocess
import StringIO

import matplotlib.pyplot as pyplot

parser = argparse.ArgumentParser(description='''
Takes output from dstat on several computers and combines them into a single figure.

This takes a single file as input.  Each line in the input file describes
the titles for each sub-plot, the data for that plot, and which statistics
to display.  For example:
	
	Server server_data.csv cpu net

extracts the cpu usage and network data from server_data.csv and plots them
on a graph named "Server".  Up to two different stat kinds may be specified.
The starting time of the plots and the length of time they should run are
additional arguments.  Output will be to the screen, unless a file is
specified with --output.

Color Key:
User + System CPU is in dark green.
Waiting CPU is in light green.

Disk writes are dark blue.
Disk reads are light blue.

Network sends are red.
Network recieves are yellow.
''')
parser.add_argument('input_file', type=argparse.FileType('r'), action='store')
parser.add_argument('--start-time', type=str, dest='start_time', action='store', required=True, help='The time at which to start plotting data.')
parser.add_argument('--length', type=int, dest='length', action='store', required=True, help='The number of seconds of data to plot.')
parser.add_argument('--output', nargs='?', type=argparse.FileType('w'), dest='output', action='store', help='If specified, the location to save a picture of the plots to.')

args = parser.parse_args()

# CPU is in light and dark green
def plot_cpu(input_file, axes):
	reader = csv.reader(input_file)
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
	
	#axes.plot(delta_times, user, color='#22AA22', linewidth=2)
	axes.plot(delta_times, user_sys, color='#22AA22', linewidth=2)
	axes.plot(delta_times, usw, color='#66FF66')
	axes.set_ylabel('CPU Utilization (%)')
	axes.set_xlabel('Time (s)')
	axes.set_ylim(top=100)

# Disk is in Dark and Light Blue
def plot_disk(input_file, axes):
	reader = csv.reader(input_file)
	
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
	
	axes.plot(delta_times, read, color='#AAAAFF', linewidth=2)
	axes.plot(delta_times, write, color='#000077', linewidth=2)
	axes.set_ylabel('Disk Activity')
	axes.set_xlabel('Time (s)')

# Network is in Red and Yellow
def plot_net(input_file, axes):
	reader = csv.reader(input_file)
	
	times = []
	recv = []
	send = []
	
	for row in reader:
		if len(row) == 0:
			continue
		if is_datetime(row[0]):
			times.append(string_to_datetime(row[0]))
			recv.append(float(row[1]))
			send.append(float(row[2]))
	
	del reader
	
	first_time = times[0]
	delta_times = [ (time - first_time).seconds for time in times]
	
	axes.plot(delta_times, recv, color='#CCCC00', linewidth=2)
	axes.plot(delta_times, send, color='#FF0000', linewidth=2)
	axes.set_ylabel('Network Activity')
	axes.set_xlabel('Time (s)')

graph_commands = []
for line in args.input_file:
	words = line.split()
	graph_commands.append({'name':words[0], 'file':words[1], 'figures':words[2:]})

for computer in graph_commands:
	f = open(computer['file'], 'rb')
	computer['time_filtered'] = subprocess.check_output(['./getDataFromTime.py', '--start-time', args.start_time, '--length', str(args.length)],stdin=f)
	f.close()


fig = pyplot.figure(figsize=(18,12))
disk_net_axes = []
#ignore node1 for setting the bounds on the plots
other_nodes_tops = []

for (idx, computer) in enumerate(graph_commands):
	axes = fig.add_subplot(len(graph_commands), 1, idx+1)
	second_axes = None
	axes.set_title(computer['name'])
	separated_stats = {}
	stat_name_list = computer['figures']
	equalize_axes = False
	for (inner_idx, stat_name) in enumerate(stat_name_list):
		script = subprocess.Popen(['./filterByStat.py', '--type', stat_name], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
		(out, err) = script.communicate(computer['time_filtered'])
		separated_stats[stat_name] = out
		
		if inner_idx == 1:
			cur_axes = pyplot.twinx(axes)
			second_axes = cur_axes
		else:
			cur_axes = axes
		if stat_name == 'cpu':
			plot_cpu(StringIO.StringIO(out), cur_axes)
		elif stat_name == 'disk':
			plot_disk(StringIO.StringIO(out), cur_axes)
			if stat_name_list[0] == 'net':
				equalize_axes = True
			if idx > 1:
				disk_net_axes.append(cur_axes)
		elif stat_name == 'net':
			plot_net(StringIO.StringIO(out), cur_axes)
			if stat_name_list[0] == 'disk':
				equalize_axes = True
			if idx > 1:
				disk_net_axes.append(cur_axes)
	
	if equalize_axes:
		max_top = max(axes.get_ylim()[1], second_axes.get_ylim()[1])
		axes.set_ylim(top=max_top)
		second_axes.set_ylim(top=max_top)
		if idx > 2:
			other_nodes_tops.append(max_top)

final_max = max(other_nodes_tops)
for axes in disk_net_axes:
	axes.set_ylim(top=final_max)

pyplot.subplots_adjust(top=0.95, bottom=0.05, hspace=0.7)

if args.output != None:
	pyplot.savefig(args.output)
else:
	pyplot.show()

