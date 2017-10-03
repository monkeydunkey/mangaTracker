'''
utilities.py
This is the common file to store the common functions
'''

import urllib2
import json
from abc import ABCMeta

DataBase = 'data.json'
scheduleFile = 'schedule.json'

def getPage(url):
  return urllib2.urlopen(url)

class scrapper:
    def __init__(self, site):
        self.site = site
        self.dataDase = DataBase

    def loadJSON(self, filename):
        try:
            with open(filename) as infile:
                return json.load(infile)
        except Exception as ex:
            raise ex.message

    def saveJSON(self, filename, data):
        try:
            with open(filename, 'w') as outfile:
                json.dump(data, outfile)
        except Exception as ex:
            raise ex.message

    def storeToDataBase(self, manga, releaseDates):
        db = self.loadJSON(self.dataDase)
        if db.get(manga, None):
            db[manga] = releaseDates
        else:
            db[manga].extend(releaseDates)
            db[manga] = list(set(db[manga]))
        self.saveJSON(self.dataDase, db)

    @property
    def getReleaseHistory(self):
        raise NotImplementedError("Individual Scrappers should implement this!")

class releaseDataGrabber:
    def __init__(self):
        self.dataSource = DataBase

    def loadJSON(self, filename):
        try:
            return json.load(open(filename))
        except Exception as ex:
            raise ex.message

    def checkExistingDataBase(self, manga):
        '''
            Check the locally stored JSON data for the release history of the
            manga
        '''
        try:
            data = self.loadJSON(self.dataSource)
            return data.get(manga, None)
        except Exception as ex:
            raise ex.message

    def

    def run(self, mangaList):
        resourceFound = [None for x in mangaList]
        for i, manga in enumerate(mangaList):
            try:
                releaseDates = self.checkExistingDataBase(manga)
                if releaseDates is None:

                else:
                    resourceFound[i] = releaseDates
            except Exception as ex:
                print 'Exception encountered while getting release dates for ' + manga + 'Skipping this Manga'
