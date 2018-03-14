import json
import urllib2
from cassandra.cluster import Cluster
import time
from matplotlib import pyplot
import numpy as np
import timeit
from functools import partial
import random

cluster = Cluster(['122.129.79.66'],port=9042)
#cluster = Cluster()
session = cluster.connect("provenancekeybenchmark")

def generateAllLinkFailure():
	start = time.time()
	rows = session.execute("SELECT * FROM node")
	for node_row in rows:
		if node_row.successor != node_row.id:
			heartBeatRows = session.execute("update heartbeat set channels='{}' where id in('"+node_row.successor+"')")

def generateAllNodeFailure():
	start = time.time()
	rows = session.execute("SELECT * FROM node")
	for node_row in rows:
			heartBeatRows = session.execute("update heartbeat set time='2017-02-13 10:20:28' where id in('"+node_row.id+"')")

while True:
	generateAllNodeFailure()