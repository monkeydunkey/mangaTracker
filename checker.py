'''
    This file is called by the job and it in turn calls the scrapper to check if
    the manga specified was released or not
'''

import mangaPandaScrapper
import sys


#Have to make this expand over a range of different scrappers
scrapper = mangaPandaScrapper.mangaPandaScrapper(-1)
manga = sys.argv[1]
print 'Checking for manga', manga
print scrapper.checkRelease(manga)
