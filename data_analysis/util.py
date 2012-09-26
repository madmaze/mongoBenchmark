#! /usr/bin/env python

import re
import datetime

datetime_year_regex = re.compile(r'(?P<year>\d\d\d\d)-(?P<month>\d\d)-(?P<day>\d\d) (?P<hours>\d\d?)\:(?P<minutes>\d\d)\:(?P<seconds>\d\d)')

datetime_regex = re.compile(r'(?P<day>\d\d)-(?P<month>\d\d) (?P<hours>\d\d?)\:(?P<minutes>\d\d)\:(?P<seconds>\d\d)')
time_regex = re.compile(r'(?P<hours>\d\d?)\:(?P<minutes>\d\d)\:(?P<seconds>\d\d)')
time_nosec_regex = re.compile(r'(?P<hours>\d\d?)\:(?P<minutes>\d\d)')

def string_to_datetime(date_str):
	today = datetime.datetime.today()
	m = re.match(datetime_year_regex, date_str)
	if m != None:
		d = m.groupdict()
		return datetime.datetime(int(d['year']), int(d['month']), int(d['day']), int(d['hours']), int(d['minutes']), int(d['seconds']))
	m = re.match(datetime_regex, date_str)
	if m != None:
		d = m.groupdict()
		return datetime.datetime(today.year, int(d['month']), int(d['day']), int(d['hours']), int(d['minutes']), int(d['seconds']))
	m = re.match(time_regex, date_str)
	if m != None:
		d = m.groupdict()
		return datetime.datetime(today.year, today.month, today.day, int(d['hours']), int(d['minutes']), int(d['seconds']))
	m = re.match(time_nosec_regex, date_str)
	if m != None:
		d = m.groupdict()
		return datetime.datetime(today.year, today.month, today.day, int(d['hours']), int(d['minutes']), 0)
	else:
		return None

def is_datetime(date_str):
	if re.match(datetime_regex, date_str) != None:
		return True
	elif re.match(datetime_year_regex, date_str) != None:
		return True
	else:
		return False
