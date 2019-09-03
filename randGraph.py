from random import *
from tkinter import *
from collections import *
import matplotlib.pyplot as plt

class Node:
    def __init__(self, nodenum):
        self.nodenum = nodenum
        self.edges = set()
##################################################################
def createPoints(): # creates dictionary of points
    nodes = {}
    for x in range(100000):
        randx = randrange(30, 720, 1)
        randy = randrange(30, 720, 1)
        nodes[x] = (randx, randy)
    return nodes
def createEdges(nodes):
    global targetavg
    edges = {}
    for x in range(len(nodes)):
        edges[x] = set()
    for x in range(len(nodes)):
        numneigh = randrange(0, targetavg+1, 1)   # determines avg degree of all nodes
        for ct in range(numneigh):  # add 0-4 neighbors (depending on rand numneigh)
            randneigh = randrange(0, len(nodes), 1)
            edges[x].add(randneigh) # add neighbor to curr node's edges
            edges[randneigh].add(x) # add curr node to neighbor's edges
    return edges
def calcData(edges):
    avg = 0
    degrees = {}
    for e in edges:
        tempdeg = len(edges[e])
        if tempdeg not in degrees:
            degrees[tempdeg] = 1
        else:
            degrees[tempdeg]+=1
        avg+=tempdeg
    orderkeys = dict(OrderedDict(sorted(degrees.items())))
    return (orderkeys, avg/len(edges))
###############################################################################################################
def main():
    global targetavg
    targetavg = 5

    nodes = createPoints()
    edges = createEdges(nodes)
    degrees, avgdeg = calcData(edges)
    print(degrees)
    print(avgdeg)

    plt.bar(range(len(degrees)), list(degrees.values()), align='center')
    plt.xticks(range(len(degrees)), list(degrees.keys()))
    plt.xlabel("Degree")
    plt.ylabel("# of vertices with degree")
    plt.title("Average degree " + str(targetavg))
    plt.show()
    # the more popular a node is, the more likely you are to make an edge with them

if __name__ == '__main__':
    main()