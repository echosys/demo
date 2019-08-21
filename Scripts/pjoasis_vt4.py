
'''
Version Apr 7 2017

Version Notes: 
This version only write list when they are completely different in cache
Display Minutes left till next run 

'''


from time import strftime, localtime
import sys
import time
import datetime
import collections

import Swebv1
from Swebv1 import Sweb
import iologgerv2
from  iologgerv2 import debuglogger

from selenium import webdriver
from selenium.webdriver.common.by import By
#from pyvirtualdisplay import Display

class Oasis(Sweb):

    def runandrecord(self):
        self.url = 'http://theoasisphoenix.com/'
        self.songnamelist = list()
        self.singernamelist = list()
        self.songnamecache = list()
        self.chromedriverrun()
        self.checklistfordup()


    def chromedriverrun(self):
        try:    
            #display = Display(visible=0, size=(800, 600))
            #display.start()
            driver = webdriver.Chrome(self.driverpath,options=self.chrome_options)  
            driver.get(self.url)
            self.logger.info("get website " + self.url)
            
            time.sleep(0.9) # Let the user actually see something!
            driver.switch_to_frame('song-history-widget')
            self.logger.info("frame switch done")
       
            xpath_title = "//span[@class = 'song-title ng-scope']/a"
            xpath_artist = "//span[@class = 'song-artist ng-scope']/a"
            list_title = driver.find_elements_by_xpath(xpath_title)
            list_artist = driver.find_elements_by_xpath(xpath_artist)
            self.logger.info("There are: {} songs and {} singers".format(len(list_title), len(list_artist) ) )
            for i in range(len(list_artist)):
                songname = list_title[i].get_attribute("text")
                self.logger.debug(songname)
                singername = list_artist[i].get_attribute("text")
                self.logger.debug('\t'+singername)
                save2json(songname, singername)

            time.sleep(3)  
            driver.quit()
            #display.stop()

        except IndexError as Ierr:
            errorcode = ("2 No data:", sys.exc_info()[0])
        except Exception as e:
            errorcode = ("2 Unexpected error in runandrecord:", sys.exc_info()[0])
            self.logger.error(errorcode)
            raise 

def save2json(songname, singername):
#key artist, value set of songs
#save as dict, output to song by artist string for dl
    print(songname, singername)

def main():
    #schedule every 15 minutes, 12 songs
    configDict = {}
    configDict['appname'] = 'oasis1'
    configDict['jsonfname'] = 'songnameswrite329.txt'
    appname = configDict['appname']

    #logger start 
    loggerinit = debuglogger()
    filename = 'debug_%s.txt' %appname
    logger1 = loggerinit.loggerstart(appname, filename)
    configDict['logger1'] = logger1

    configDict['driverpath'] = 'depoly'
    
    oasis1 = Oasis(configDict)
    oasis1.driver_init()
    td = datetime.timedelta(minutes = 15)
    secondsInt = int(td.total_seconds())
    Swebv1.runbytimeinterval(oasis1, secondsInt)

if __name__ == '__main__':
    main()





