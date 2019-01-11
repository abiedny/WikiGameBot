#!/usr/bin/python

import sys
import asyncio
from Page import Page, Tree

start = "Simon_Sechter"
end = "German_Language"

currentPage = Page('/wiki/'+start, '/wiki/'+end, '/wiki/'+start)
tree = Tree(currentPage)
print(tree.bfs())