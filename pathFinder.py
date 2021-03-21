from bs4 import BeautifulSoup
import urllib3
import validators
import sys

wikipediaUrlPrefix = 'https://en.wikipedia.org'


def getPageSoup(url):
    validators.url(url)
    http = urllib3.PoolManager()
    response = http.request('Get', url)
    page_source = response.data
    soup = BeautifulSoup(page_source, 'html.parser')
    return soup


def getListOfWikipediaPages(soup):
    return soup.select('a[href^="/wiki/"]')


class wikipediaPage():
    def __init__(self, url: str, parent):
        self.parent = parent
        self.url = url
        self.children = None
        self.name = None
        self.soup=None
    def getSoup(self):
        if self.soup ==None:
            self.soup = getPageSoup(self.url)
        return self.soup

    def getChildren(self):
        if self.children != None:
            return self.children

        listWikipediaPages = []

        for anchor in getListOfWikipediaPages(self.getSoup()):
            listWikipediaPages.append(wikipediaPage(wikipediaUrlPrefix+anchor.get('href'), self))

        self.children = listWikipediaPages
        return self.children

    def getName(self):
        if self.name != None:
            return self.name

        self.name = self.getSoup().select('#firstHeading')[0].getText()
        return self.name
    
    def getNameFromUrl(self):
        name =self.url.split('/')[-1]
        if name.find('#')==-1:
            return name.replace('_', ' ')
        return name[:name.find('#')].replace('_',' ')

    def __eq__(self, other):
        if isinstance(other, wikipediaPage):
            if self.getNameFromUrl()== other.getNameFromUrl():
                return self.getName() == other.getName()
        return False


def findPath(urlStart, urlEnd):
    startPage = wikipediaPage(urlStart, parent=None)
    endPage = wikipediaPage(urlEnd, None)
    visited = set()
    queue=[startPage]

    while True:
        for page in queue:
            if page == endPage:
                print(getPast(page))
                return
    
        page = queue.pop(0)
        if page.getNameFromUrl() in visited:
            continue
        
        visited.add(page.getNameFromUrl())
        for child in page.getChildren():
            if child == endPage:
                print(getPast(child))
                return 
        queue.extend(page.getChildren())
   
    

        

def getPast(endPage:wikipediaPage):
    path=[]
    path_name=[]
    while endPage!=None:
        path.append(endPage)
        endPage=endPage.parent
    path = path[::-1]
    path_name.append(path[0].getName())
   
    for i in range(1,len(path),1):
        soup = getPageSoup(path[i-1].url)
        anchors = soup.select(f'a[href="{path[i].url[path[i].url.find("/wiki/"):]}"]')
        path_name.append(anchors[0].getText())
    return path_name
   

findPath(f"{sys.argv[1]}",f"{sys.argv[2]}")
