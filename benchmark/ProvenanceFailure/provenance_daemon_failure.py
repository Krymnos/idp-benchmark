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
datapair = {}
def findProvenanceFailure():
	start = time.time()
	rows = session.execute("SELECT * FROM node")
	for node_row in rows:
		countRows = session.execute("select count(*) from provenancetable where nodeid='"+node_row.id+"' allow filtering")
		for count_row in countRows:
				if  node_row.id in datapair:
					a = datapair[node_row.id]
					if count_row.count > a:
						print("Provenance Daemon in Node "+node_row.id+" active.")
					else:
						print("Provenance Daemon in Node "+node_row.id+" failed.")
				else:
					print("Initializing...")
				datapair[node_row.id] = count_row.count
	#end = time.time()
	#time.sleep(5)
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
        f = open("results/provenancefailure.txt","a")
        f.write(str(i)+","+str(t)+"\n")
        f.close()
    #p1 = pyplot.plot(x, y, 'o')

def main():
    print('Analyzing Provenance system for Provenance Daemon failures...')

    plotTC(findProvenanceFailure, 0, 216, 60, 1)
    #pyplot.show()

# call main
if __name__ == '__main__':
	main()
