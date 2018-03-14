import json
import urllib2
from cassandra.cluster import Cluster
import time
#from matplotlib import pyplot
import numpy as np
import timeit
from functools import partial
import random
import datetime
from sys import argv

cluster = Cluster([argv[2]],port=9042)
#cluster = Cluster()
session = cluster.connect("provenancekey")
timepair = {}

def findPipelineFailure():
	start = time.time()
	rows = session.execute("SELECT * FROM node")
	for node_row in rows:
		heartBeatRows = session.execute("SELECT * FROM heartbeat where id='"+node_row.id+"'")
		for heartbeat_row in heartBeatRows:
			if heartbeat_row.id == node_row.id:
				if str(heartbeat_row.id) in timepair:
					a = timepair[str(heartbeat_row.id)]
					b = a + datetime.timedelta(0,30)
					if heartbeat_row.pldaemon > b:
						print("Pipeline Daemon on node "+node_row.id+" active.")
					else:
						print("Pipeline Daemon on node "+node_row.id+" failed.")
				else:
					print("Initializing...")
				timepair[str(heartbeat_row.id)] = heartbeat_row.pldaemon
	time.sleep(30)
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
        f = open("results/pipelinefailure.txt","a")
        f.write(str(i)+","+str(t)+"\n")
        f.close()
    #p1 = pyplot.plot(x, y, 'o')

def main():
    print('Analyzing Provenance system for Pipeline Daemon failures...')

    plotTC(findPipelineFailure, 0, 216, 60, 1)
    #pyplot.show()

# call main
if __name__ == '__main__':
	main()