# Use permutations with small groups of nodes to get shortest hamiltonian cycle

import sys
import itertools
from math import *
from tkinter import *
from collections import *
from time import *

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
    infile = open("DAU.txt", 'r')
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
    adapted_w = canvas.winfo_width()*0.85   # so that img doesn't take up full canvas on the border
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
def DFS(start, edges, distances):  # start is nodenum of first node; edges is dict of all nodes' edges connecting it to other nodes
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
            children = orderChildren(children, temp.path[-1], distances)
            for c in children:
                newN = Node(c, temp)
                fringe.append(newN)
    return
def orderChildren(children, startnode, distances):
    temp = [(distances[c][startnode], c) for c in children]     # temp = [(distance, nodenum), ...]
    # sort from greatest dist to smallest dist from startnode because when added onto stack in DFS, the smallest
    # distance will be added last, meaning it'll be popped off first --> prioritizes finding shortest path distance
    temp.sort(reverse=True)
    newchildren = [t[1] for t in temp]
    return newchildren
def orientPath(path):
    newpath, behind = [0], []   # behind contains all other nodes following node 0
    start = path.index(0)
    i = start+1
    while i%len(path) != start:
        behind.append(path[i%len(path)])
        i+=1
    if behind[0] > behind[-1]:  behind.reverse()    # so that second node is the smaller val than last node
    newpath+=behind
    return newpath
def calcPathDistance(path, distances):
    totaldist = 0
    start = 0
    i, mod = start+1, len(path)
    while i%mod != start:
        totaldist+=distances[path[i%mod]][path[(i+1)%mod]]
        i+=1
    totaldist+=distances[path[i%mod]][path[(i+1)%mod]]
    return totaldist
def createImage(nodes2):
    global canvas, root
    for k in nodes2:
        x1, y1 = nodes2[k][0]-2, nodes2[k][1]-2
        x2, y2 = nodes2[k][0]+2, nodes2[k][1]+2
        canvas.create_oval(x1, y1, x2, y2, fill='black', outline='')
        # canvas.create_text((x1-4, y1-4), text=str(k))
    root.update()
def drawHamiltonianCycle(path, nodes2):
    global root, canvas
    createImage(nodes2)
    start = 0   # the index to start at (the front)
    i, mod = start+1, len(path)
    while i%mod != start:
        x1, y1 = nodes2[path[i%mod]][0], nodes2[path[i%mod]][1]
        x2, y2 = nodes2[path[(i+1)%mod]][0], nodes2[path[(i+1)%mod]][1]
        canvas.create_line(x1, y1, x2, y2, fill='red', width=1)
        i+=1
    x1, y1 = nodes2[path[i%mod]][0], nodes2[path[i%mod]][1]
    x2, y2 = nodes2[path[(i+1)%mod]][0], nodes2[path[(i+1)%mod]][1]
    canvas.create_line(x1, y1, x2, y2, fill='red', width=1)
def reverse_n1_n2(path, n1, n2):
    rev = []
    start, end = path.index(n1), path.index(n2)
    i = start
    while i%len(path) != (end+1)%len(path):
        rev.append(path[i%len(path)])
        i+=1
    rev.reverse()
    newpath = []
    while i%len(path) != start%len(path):
        newpath.append(path[i%len(path)])
        i+=1
    newpath = rev + newpath
    return newpath
def detanglePath(path, distances):
    repeat = True
    newpath = path
    mod = len(newpath)
    while repeat:
        repeat = False
        for i in range(0, mod):
            for j in range(i+2, i+mod-1):
                n1, n2 = newpath[i%mod], newpath[(i+1)%mod]     # update ALL nodes EVERY time bc each time unscrambled, the nodes at those indexes may change
                n3, n4 = newpath[j%mod], newpath[(j+1)%mod]
                d12, d34 = distances[n1][n2], distances[n3][n4]
                d13, d24 = distances[n1][n3], distances[n2][n4]
                if d12+d34 > d13+d24:   # AKA there's an intersection
                    newpath = reverse_n1_n2(newpath, n2, n3)
                    repeat = True
    return newpath
def shortestPermutePath(path, distances):
    newpath = path
    mod = len(newpath)
    newpath2 = newpath+newpath
    n = 5
    ALLPERMS = []
    for i in range(0, mod):
        section = newpath2[i:(i+n)]
        back = newpath2[(i+n):(i+mod)]
        L = list(itertools.permutations(section))
        permsection = [list(t) for t in L]
        ALLPERMS += [p+back for p in permsection]
    shortest = min(ALLPERMS, key=lambda k: calcPathDistance(k, distances))
    return shortest
###################################################################################################################
def firstProcess():
    global root, canvas
    root = Tk()
    canvas = Canvas(root, width=750, height=750, highlightthickness=0, background="white", highlightbackground="white")
    canvas.pack()
    root.update()
    ##
    nodes, distances, edges = getFileNodes()
    nodes2 = makeConvertedNodes(nodes)  # canvas-adapted node coordinates
    ##
    nSOLN = DFS(0, edges, distances)
    origpath = orientPath(nSOLN.path)
    print(origpath)
    print(calcPathDistance(origpath, distances))
    drawHamiltonianCycle(origpath, nodes2)
    ##
    root.bind("<KeyPress>", lambda e: secondProcess(origpath, distances, nodes2))   # on any keypress, start second process
    root.update()
    root.mainloop()
def secondProcess(prevpath, distances, nodes2):
    global root, canvas
    root.destroy()
    root = Tk()
    canvas = Canvas(root, width=750, height=750, highlightthickness=0, background="white", highlightbackground="white")
    canvas.pack()
    root.update()
    ##
    newpath = detanglePath(prevpath, distances)
    # newpath = shortestPermutePath(prevpath, distances)
    newpath = orientPath(newpath)
    print(newpath)
    print(calcPathDistance(newpath, distances))
    drawHamiltonianCycle(newpath, nodes2)
    ##
    root.focus_force()  # brings canvas window into focus
    root.bind("<KeyPress>", lambda e: thirdProcess(newpath, distances, nodes2))  # on any keypress, close canvas window
    root.update()
    root.mainloop()
def thirdProcess(prevpath, distances, nodes2):
    global root, canvas
    root.destroy()
    root = Tk()
    canvas = Canvas(root, width=750, height=750, highlightthickness=0, background="white", highlightbackground="white")
    canvas.pack()
    root.update()
    ##
    # newpath = detanglePath(prevpath, distances)
    tic = time()
    newpath = shortestPermutePath(prevpath, distances)
    newpath = orientPath(newpath)
    toc = time()
    print(newpath)
    print(calcPathDistance(newpath, distances))
    # print("Time: ", toc-tic)
    drawHamiltonianCycle(newpath, nodes2)
    ##
    root.focus_force()  # brings canvas window into focus
    root.bind("<KeyPress>", lambda e: root.destroy())  # on any keypress, close canvas window
    root.update()
    root.mainloop()

###################################################################################################
def main():
    firstProcess()

if __name__ == '__main__':
    main()