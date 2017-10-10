'''
This is the entry point for the system
Control Flow:
1. Load up the config.json file to read the manga list
2. For each of the manga check the downloaded dataset, if not present fetch last 6 months of data from the site
3. Pass the release history of the manga to find an approximate release schedule. - To Implement
4. Set up corn jobs according to the schedule with the fallback specified by the user
'''

import utilities
import json
from crontab import CronTab
import scheduler
import os, getpass
def setWeeklySchedule(manga, schedule):
    cron   = CronTab(getpass.getuser())
    job  = cron.new(command='python checker.py ' + manga + ' >> mangaFound.txt')
    job.dow.on(schedule[:3].upper())
    job.enable()
    cron.write()

configFile = 'config.json'
mangaList = None
config = None
with open(configFile) as e:
    config = json.load(e)

mangaList = config['mangas']
lookback = config['Lookback']
releaseChecker = utilities.releaseDataGrabber()
releaseHistory = releaseChecker.run(mangaList, lookback)
print 'The release history is', releaseHistory
schedules = scheduler.scheduleSearch()
for i, sch in enumerate(schedules):
    if type(sch) == type({}):
        if sch['type'] == 'Weekly':
            setWeeklySchedule(mangaList[i], sch['dow'])
        else:
            print 'Non weekly schedule not implemented yet'
    else:
        print 'There was no schedule returned'
