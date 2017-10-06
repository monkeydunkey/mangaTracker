'''
Base Class implementation for site scrappers
'''

import json

class scrapper(object):
    def __init__(self, site):
        self.site = site
        self.dataDase = 'data.json'

    def loadJSON(self, filename):
        try:
            with open(filename) as infile:
                return json.load(infile)
        except Exception as ex:
            raise ex

    def saveJSON(self, filename, data):
        try:
            with open(filename, 'w') as outfile:
                json.dump(data, outfile)
        except Exception as ex:
            raise ex

    def storeToDataBase(self, scrappedData):
        db = self.loadJSON(self.dataDase)
        for manga in scrappedData.keys():
            if db.get(manga, None) is None:
                db[manga] = scrappedData[manga]
            else:
                db[manga].extend(scrappedData[manga])
                db[manga] = list(set(db[manga]))
        self.saveJSON(self.dataDase, db)

    @property
    def getReleaseHistory(self):
        raise NotImplementedError("Individual Scrappers should implement this!")
