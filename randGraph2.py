from random import *
from tkinter import *
from collections import *
import matplotlib.pyplot as plt
from numpy.random import choice
# print(choice(elements, p=weights))

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
def createDegrees(nodes):
    global targetavg
    degrees = {}
    for x in range(len(nodes)): # default 1, aka equal chance of neighboring with any node
        degrees[x] = 1
    for x in range(len(nodes)):
        print(x)
        numneigh = randrange(0, targetavg+1, 1)
        # weighted = getweighted(degrees)
        for ct in range(numneigh):
            randneigh = getRandNeigh(degrees)
            degrees[x]+=1
            degrees[randneigh]+=1
    return degrees
def getRandNeigh(degrees):
    elements = list(degrees.keys())
    s = sum([degrees[d] for d in degrees])
    weights = [degrees[x]/s for x in degrees]
    # weights = list(degrees.values())
    randneigh = choice(elements, p=weights)
    return randneigh
    # for d in degrees:
    #     L+=[d for x in range(degrees[d])]
    # return L
    # return L[randrange(0, len(L), 1)]
# def createEdges(nodes):
#     global avgdeg
#     edges = {}
#     for x in range(len(nodes)):
#         edges[x] = set()
#     for x in range(len(nodes)):
#         numneigh = randrange(0, avgdeg+1, 1)   # determines avg degree of all nodes
#         for ct in range(numneigh):  # add 0-4 neighbors (depending on rand numneigh)
#             randneigh = randrange(0, len(nodes), 1)
#             edges[x].add(randneigh) # add neighbor to curr node's edges
#             edges[randneigh].add(x) # add curr node to neighbor's edges
#     return edges
def calcData(degrees):
    avg = 0
    for d in degrees:
        avg+=degrees[d]
    return avg/len(degrees)
###############################################################################################################
def main():
    global targetavg
    targetavg = 5

    nodes = createPoints()
    degrees = createDegrees(nodes)
    avgdeg = calcData(degrees)
    print(degrees)
    print(avgdeg)

    plt.bar(range(len(degrees)), list(degrees.values()), align='center')
    plt.xticks(range(len(degrees)), list(degrees.keys()))
    plt.xlabel("Degree")
    plt.ylabel("# of vertices with degree")
    plt.title("Average degree " + str(targetavg))
    plt.show()

    # d = {0:1, 1:4, 2:3}
    # print(list(d.keys()))
    # print(list(d.values()))

    # temp = {}
    # for x in range(10):
    #     temp[x] = x
    # print(getRandNeigh(temp))

    # the more popular a node is, the more likely you are to make an edge with them
    # try it for avgdeg 4 and 5

if __name__ == '__main__':
    main()