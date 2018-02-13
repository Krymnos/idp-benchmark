import json
import urllib2
from cassandra.cluster import Cluster
import time
from matplotlib import pyplot
import numpy as np
import timeit
from functools import partial
import random
import datetime

cluster = Cluster(['122.129.79.66'],port=9042)
#cluster = Cluster()
session = cluster.connect("provenancekeybenchmark")
timepair = {}

def findLinkFailure():
	start = time.time()
	rows = session.execute("SELECT * FROM node")
	for node_row in rows:
		neighbour = False
		nodeLinkActive = False
		node1Active = False
		node2Active = False
		if node_row.successor != node_row.id:
			heartBeatRows = session.execute("SELECT * FROM heartbeat where id in ('"+node_row.id+"','"+node_row.successor+"')")
			neighbour = True
		else:
			heartBeatRows = session.execute("SELECT * FROM heartbeat where id='"+node_row.id+"'")
		for heartbeat_row in heartBeatRows:
			if heartbeat_row.id == node_row.id:
				node1Active = True
			if neighbour == True:
				#if heartbeat_row.id == node_row.successor:
					node2Active = True
					sentList = heartbeat_row.channels
					for sentneighbour in sentList:
						sentneighbourlist = sentneighbour.split(":")
						if node_row.id in sentneighbourlist:
							if str(heartbeat_row.id) in timepair:
								a = timepair[str(heartbeat_row.id)]
								b = a + datetime.timedelta(0,30)
								if sentList[sentneighbour] > b:
									nodeLinkActive = True
								else:
									nodeLinkActive = False
							else:
								nodeLinkActive = True
							timepair[str(heartbeat_row.id)] = sentList[sentneighbour]
		if node1Active == True & node2Active == True & nodeLinkActive == True:
			print("Link active between "+node_row.id+" and "+node_row.successor)
		elif nodeLinkActive == False:
			print("Link broken between "+node_row.id+" and "+node_row.successor)
	#time.sleep(30)
	end = time.time()
	print("Total Time taken: " + str(end - start))

#while True:
#	findLinkFailure()
#	time.sleep(5)

def plotTC(fn, nMin, nMax, nInc, nTests):
    x = []
    y = []
    for i in range(nMin, nMax, nInc):
        testNTimer = timeit.Timer(partial(fn))
        t = testNTimer.timeit(number=nTests)
        x.append(i)
        y.append(t)
    p1 = pyplot.plot(x, y, 'o')

def main():
    print('Analyzing Provenance system for link failures...')

    plotTC(findLinkFailure, 60, 36000, 60, 1)
    pyplot.show()

# call main
if __name__ == '__main__':
	main()