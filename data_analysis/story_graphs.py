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

parser = argparse.ArgumentParser()
parser.add_argument('input_file', type=argparse.FileType('r'), action='store')
parser.add_argument('--start-time', type=str, dest='start_time', action='store', required=True)
parser.add_argument('--length', type=int, dest='length', action='store', required=True)
parser.add_argument('--output', nargs='?', type=argparse.FileType('w'), default=sys.stdout, dest='output', action='store')

args = parser.parse_args()

graph_commands = []


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
	
	axes.plot(delta_times, user, color='#FF0000')
	axes.plot(delta_times, user_sys, color='#00FF00')
	axes.plot(delta_times, usw, color='#5555FF')
	axes.set_ylabel('CPU Utilization (%)')
	axes.set_xlabel('Time (s)')

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
	
	axes.plot(delta_times, read, color='#5555FF', linewidth=2)
	axes.plot(delta_times, write, color='#00FF00', linewidth=2)
	axes.set_ylabel('Disk Activity')
	axes.set_xlabel('Time (s)')

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
	
	axes.plot(delta_times, recv, color='#5555FF', linewidth=2)
	axes.plot(delta_times, send, color='#00FF00', linewidth=2)
	axes.set_ylabel('Network Activity')
	axes.set_xlabel('Time (s)')

for line in args.input_file:
	words = line.split()
	graph_commands.append({'name':words[0], 'file':words[1], 'figures':words[2:]})

for computer in graph_commands:
	f = open(computer['file'], 'rb')
	computer['time_filtered'] = subprocess.check_output(['./getDataFromTime.py', '--start-time', args.start_time, '--length', str(args.length)],stdin=f)
	f.close()


fig = pyplot.figure()
for (idx, computer) in enumerate(graph_commands):
	axes = fig.add_subplot(len(graph_commands), 1, idx+1)
	separated_stats = {}
	stat_name_list = computer['figures']
	for (idx, stat_name) in enumerate(stat_name_list):
		script = subprocess.Popen(['./filterByStat.py', '--type', stat_name], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
		(out, err) = script.communicate(computer['time_filtered'])
		#print out
		separated_stats[stat_name] = out
		
		if idx == 1:
			cur_axes = pyplot.twinx(axes)
		else:
			cur_axes = axes
		if stat_name == 'cpu':
			plot_cpu(StringIO.StringIO(out), cur_axes)
		elif stat_name == 'disk':
			plot_disk(StringIO.StringIO(out), cur_axes)
		elif stat_name == 'net':
			plot_net(StringIO.StringIO(out), cur_axes)

pyplot.show()
	

