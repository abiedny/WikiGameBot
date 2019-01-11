#!/usr/bin/python

import sys
from Page import Page, Tree
import time

start = "2018_Democratic_Republic_of_the_Congo_general_election"
end = "Universal_suffrage"

startT = time.time()
currentPage = Page('/wiki/'+start, '/wiki/'+end, '/wiki/'+start)
tree = Tree(currentPage)
print(tree.bfs())
endT = time.time()
print("Time Elapsed: " + str(endT-startT) + "seconds")