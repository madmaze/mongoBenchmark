#! /usr/bin/env python

import pymongo
import os

file_list = os.listdir('/home/ubuntu/s3/')

for path in file_list:
	print path
