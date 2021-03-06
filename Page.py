import requests
from bs4 import BeautifulSoup
import asyncio
from threading import Thread
from threading import activeCount
import multiprocessing.dummy

#Creating a page object inherently checks for the final URL
class Page:
    def __init__(self, pageURL, endURL, path):
        result = requests.get('https://en.wikipedia.org' + pageURL)
        soup = BeautifulSoup(result.content, 'html.parser')
        self.pageURL = pageURL
        self.endURL = endURL
        self.found = False
        self.path = path

        self.links = []
        for link in soup.find_all('a'):
            linkText = link.get('href')
            if linkText is None:
                continue
            elif ':' in linkText:
                continue
            elif '(disambiguation)' in linkText:
                continue
            elif linkText.startswith('/wiki/'):
                self.links.append(linkText)
                if linkText == endURL:
                    self.found = True
        #spawn a new thread and queue up the buildNext work on it
        if activeCount() < 500:
            self.builder = Thread(None, self.buildNext)
            self.builder.start()

    #switches the array of link strings to an array of page objects
    def buildNext(self):
        #Make a process pool to do this map quickly
        p = multiprocessing.dummy.Pool(100)
        self.links = p.map(self.__toPage, self.links)
        return True

    def __toPage(self, link):
        return Page(link, self.endURL, self.path+"->"+link)

#the collection of pages, the tree
class Tree:
    def __init__(self, root):
        self.root = root #Should be a page object

    def bfs(self):
        queue = [] 
        queue.append(self.root)
        while queue:
            page = queue.pop(0)
            if page.found:
                return page.path
            elif not hasattr(page, 'builder'):
                #We hit the thread limit and this page is a dead end?
                pass
            elif len(queue) == 0:
                #if queue is empty, build next layer and add it to the queue
                page.builder.join() #block this thread until page.links is built
                if not page.builder.is_alive():
                    queue.extend(page.links)