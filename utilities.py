'''
utilities.py
This is the common file to store the common functions
'''

import urllib2
import json

DataBase = 'data.json'
scheduleFile = 'schedule.json'

def getPage(url):
  return urllib2.urlopen(url)


class scrapper:
    def __init__(self, site):
        self.site = site
        self.dataSource = DataBase

    def loadJSON(filename):
        try:
            return json.load(open(filename))
        except Exception as ex:
            raise ex.message

    def checkExistingDataBase(manga):
        '''
            Check the locally stored JSON data for the release history of the
            manga
        '''
        try:
            data = self.loadJSON(self.dataSource)
            return data.get(manga, None)
        except Exception as ex:
            raise ex.message

    def run(mangaList):
        
