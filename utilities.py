'''
utilities.py
This is the common file to store the common functions
'''

import urllib2
import json
from abc import ABCMeta
import mangaPandaScrapper
DataBase = 'data.json'
scheduleFile = 'schedule.json'


class releaseDataGrabber:
    def __init__(self):
        self.dataSource = DataBase

    def checkExistingDataBase(self, manga):
        '''
            Check the locally stored JSON data for the release history of the
            manga
        '''
        try:
            with open(self.dataSource) as e:
                data = json.load(e)
            return data.get(manga, None)
        except Exception as ex:
            raise ex

    def run(self, mangaList, lookback):
        resourceFound = [None for x in mangaList]
        for i, manga in enumerate(mangaList):
            try:
                releaseDates = self.checkExistingDataBase(manga)
                if releaseDates is None:
                    scrapper = mangaPandaScrapper.mangaPandaScrapper(lookback)
                    scrapper.getReleaseHistory()
                    resourceFound[i] = self.checkExistingDataBase(manga)
                else:
                    resourceFound[i] = releaseDates
            except Exception as ex:
                print 'Exception encountered while getting release dates for ' + manga + 'Skipping this Manga', ex.message
                raise
        return resourceFound
