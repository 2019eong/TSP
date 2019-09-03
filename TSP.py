# Find a Hamiltonian cycle, display it, and kill it on keypress

import sys
from math import *
from tkinter import *
from collections import *

global canvas, root
class Node:
    def __init__(self, nodenum, parent):
        self.nodenum = nodenum
        self.parent = parent
        if parent is None:
            self.path = [nodenum]
        elif parent is not None:
            self.path = self.parent.path.copy()
            self.path.append(nodenum)
##############################################################################################
def calcd(x1, y1, x2, y2):
    x1, y1 = float(x1), float(y1)
    x2, y2 = float(x2), float(y2)
    # R  = 3958.76 # radius of earth in mi
    R = 6371 # radius in km
    y1 *= pi/180.0
    x1 *= pi/180.0
    y2 *= pi/180.0
    x2 *= pi/180.0
    return acos( sin(y1)*sin(y2) + cos(y1)*cos(y2)*cos(x2-x1) ) * R
def getFileNodes():
    infile = open("KAD.txt", 'r')
    nodes, distances, edges = {}, {}, {}
    with infile as f:
        next(f)
        nodenum = 0
        for line in infile:
            coord = line.strip().split(" ")
            nodes[nodenum] = (float(coord[0])/1000, float(coord[1])/1000)
            nodenum+=1
    for f in nodes:
        long1, lat1 = nodes[f]
        distdic, edgelist = {}, []
        for x in range(nodenum):    # nodes 0-37
            if x != f:
                long2, lat2 = nodes[x]
                distdic[x] = calcd(long1, lat1, long2, lat2)
                edgelist.insert(0, x)
                # edgelist.append(x)
        distances[f] = distdic
        edges[f] = edgelist
    # distances = {node1num : {node2num : distance}}
    # edges = {node1num : [node#num, ...]}
    return nodes, distances, edges
def makeConvertedNodes(nodes):  # converts node values to fit properly in canvas
    global canvas, root
    nodes2 = {}
    lat, long = set(), set()
    for x in nodes:
        lat.add(nodes[x][1])
        long.add(nodes[x][0])
    minLat, minLong = min(lat), min(long)
    maxLat, maxLong = max(lat), max(long)
    diffLat, diffLong = maxLat-minLat, maxLong-minLong
    ##
    adapted_w = canvas.winfo_width()*0.85
    adapted_h = canvas.winfo_height()*0.85
    border_w = (canvas.winfo_width()-adapted_w)/2
    border_h = (canvas.winfo_height()-adapted_h)/2
    for k in nodes:
        nodes2[k] = (adapted_w/diffLong)*(nodes[k][0]-minLong)+border_w, -(adapted_h/diffLat)*(nodes[k][1]-maxLat)+border_h
    return nodes2
def goal_test(node, numofnodes):
    path = node.path
    for n in range(numofnodes):
        if n not in path:   return False
    return True
def DFS(start, edges):  # start is nodenum of first node; edges is dict of all nodes' edges connecting it to other nodes
    n = Node(start, None)
    fringe = deque()
    fringe.append(n)
    while len(fringe) > 0:
        temp = fringe.pop()
        if goal_test(temp, len(edges)):
            return temp
        else:
            # children are list of all other UNVISITED nodenums that current node is connected to
            children = [n for n in edges[temp.nodenum] if n not in temp.path]
            for c in children:
                newN = Node(c, temp)
                fringe.append(newN)
    return
def orientPath(path):
    newpath = [0]
    if path[1] < path[-1]:  return path
    else:   newpath+=path[:0:-1]
    return newpath
def calcPathDistance(path, distances):
    pathdistance = 0
    for x in range(len(path)-1):
        pathdistance+=distances[path[x]][path[x+1]]
    pathdistance+=distances[path[x+1]][0]
    return pathdistance
def createImage(nodes2):
    global canvas, root
    for k in nodes2:
        canvas.create_oval(nodes2[k][0]-2, nodes2[k][1]-2, nodes2[k][0]+2, nodes2[k][1]+2, fill='black', outline='')
    root.update()
def drawHamiltonianCycle(path, nodes2):
    global root, canvas
    createImage(nodes2)
    for x in range(len(path)-1):
        x1, y1 = nodes2[path[x]][0], nodes2[path[x]][1]
        x2, y2 = nodes2[path[x+1]][0], nodes2[path[x+1]][1]
        canvas.create_line(x1, y1, x2, y2, fill="red", width=1)
    x1, y1 = nodes2[path[x+1]][0], nodes2[path[x+1]][1]
    x2, y2 = nodes2[0][0], nodes2[0][1]
    canvas.create_line(x1, y1, x2, y2, fill="red", width=1)
def fullProcess():
    global root, canvas
    root = Tk()
    root.bind("<KeyPress>", lambda e: root.destroy())  # on any keypress, close canvas window
    canvas = Canvas(root, width=500, height=600, highlightthickness=0, background="white", highlightbackground="white")
    canvas.pack()
    root.update()
    ##
    nodes, distances, edges = getFileNodes()
    nodes2 = makeConvertedNodes(nodes)  # canvas-adapted node coordinates
    ##
    nSOLN = DFS(0, edges)
    path = orientPath(nSOLN.path)
    print(path)
    pathdistance = calcPathDistance(path, distances)
    print(pathdistance)
    ##
    drawHamiltonianCycle(path, nodes2)
    root.update()
    root.mainloop()

def main():
    fullProcess()

if __name__ == '__main__':
    main()

##### 1)  Read in the points, computing all pairwise distances.
##### 2)  Display any Hamiltonian Cycle of your choosing using TKinter (or other graphics package that you can easily update).
##### 3)  Be able to dismiss this window by pressing any key
##### 4)  In the command window, you should output the Hamiltonian cycle you displayed
##### 5)  Also show the distance of your Hamiltonian cycle