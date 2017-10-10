'''
Scrapper to scrap the release history from manga panda
'''
import urllib2
from bs4 import BeautifulSoup as bs
from scrapper import scrapper
from datetime import datetime, timedelta
import dateparser

class mangaPandaScrapper(scrapper):
    def __init__ (self, lookback):
        self.url = 'http://www.mangapanda.com/latest/'
        self.today = datetime.now().date()
        self.endDate = self.today + timedelta(-1 * lookback)
        super(self.__class__, self).__init__('mangaPanda')

    def parseData(self, data):
        '''
            Parse the data scrapped from the site
        '''
        mangaList = {}
        for en in data:
            releaseDate = str(dateparser.parse(en.select('.c1')[0].text).date())
            manga = en.select('.chapter')[0].text
            mangaList[manga] = mangaList.get(manga, []) + [releaseDate]
        self.storeToDataBase(mangaList)


    def getData(self, url):
        print 'Fetching Data for url', url
        page = urllib2.urlopen(url).read()
        soup = bs(page)
        releaseData = soup.select('table.updates tr')
        nextPagelink = str((int(soup.select('#sp strong')[0].text) - 2) * 100)
        return releaseData, nextPagelink

    def getLastReleaseDate(self, data):
        return dateparser.parse(data[-1].select('.c1')[0].text).date()

    def getReleaseHistory(self):
        '''
        The function to scrap the last 6 months of data from mangaPanda
        '''
        data, nextLink = self.getData(self.url)
        oldestRelease = self.getLastReleaseDate(data)
        while oldestRelease > self.endDate:
            '''
                Loop and find the release objects
            '''
            releaseDates, nextLink = self.getData(self.url + nextLink)
            data.extend(releaseDates)
            oldestRelease = self.getLastReleaseDate(releaseDates)

        self.parseData(data)
