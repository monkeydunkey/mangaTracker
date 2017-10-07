'''
File to figure out the release schedule of a Manga
'''

from datetime import datetime, timedelta
import dateparser
import json
import calendar
import pandas as pd

config = 'config.json'
dataFile = 'data.json'

def loadFile(f):
    return json.load(open(f))


def getSchedule(manga, db, lookback):
    if db.get(manga, None) is None:
        return "There are no entries for " + manga
    else:
        '''
        Get the average days between 2 releases and once you have that we can
        work on getting the exact date
        '''
        releaseDates = map(lambda x: datetime.strptime(x, '%Y-%m-%d'), db[manga])
        daysbetween = 0
        schedule = None
        daysBetween = {}
        maxCount = 0
        mostFrequentDaysBetween = None
        for i in range(len(releaseDates) - 2 , -1, -1):
            betw = (releaseDates[i] - releaseDates[i + 1]).days
            daysBetween[betw]  = daysBetween.get(betw, 0) + 1
            if maxCount < daysBetween[betw]:
                mostFrequentDaysBetween = betw
                maxCount = daysBetween[betw]

        if mostFrequentDaysBetween <= 8:
            #So the schedule has to be weekly
            releaseDays = map(lambda x: x.weekday(), releaseDates)
            averageDayOfWeek = float(reduce(lambda x, y: x+y, releaseDays))/len(releaseDays)
            approxSchedule = round(averageDayOfWeek)
            schedule = 'Weekly on ' + calendar.day_name[int(approxSchedule)]
        else:
            schedule = 'Non Weekly scheduler not Implemented Yet'
        '''
        elif averageDaysBetween <= 17:
            #So the release schedule is biweekly
        '''
        return schedule


def scheduleSearch():
    '''
    Figure out of the schedule of each of the mangas in the config
    '''
    configData = loadFile(config)
    mangaList = configData['mangas']
    db = loadFile(dataFile)
    for manga in mangaList:
        print getSchedule(manga, db, configData['Lookback'])


if __name__ == '__main__':
    scheduleSearch()
