
'''
This version last modified on Apr 29 2018

Version Notes: 

Deploy Notes

Todo


'''


import sys
import time
from time import strftime, localtime
import datetime
import collections
import codecs
import os 
import json

from Swebv1 import Sweb
import Swebv1
import iologgerv2
from iologgerv2 import debuglogger

import pyautogui
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
#from pyvirtualdisplay import Display

class Oasis(Sweb):
    def addsettings(self):
        """Chrome options for printing """ 
        settings = {
            "appState": {
                "recentDestinations": [{
                    "id": "Save as PDF",
                    "origin": "local"
                }],
                "selectedDestinationId": "Save as PDF",
                "version": 2
            }  
        }
        
        prefs = {'printing.print_preview_sticky_settings': json.dumps(settings)}
        self.chrome_options.add_experimental_option('prefs', prefs)
        #self.chrome_options.AddUserProfilePreference("printing.print_preview_sticky_settings.appState", "{\"version\":2,\"isGcpPromoDismissed\":false,\"selectedDestinationId\":\"Save as PDF\"");
        #self.chrome_options.add_argument('--kiosk-printing')  #this allows auto lick print
        
        """Task URl info""" 
        self.url1 = 'https://www.wileyplus.com/Section/id-406740.html?nocache=1'

    def runandrecord(self):
        try:    
            driver = webdriver.Chrome(self.driverpath,options=self.chrome_options) 
            driver.get(self.url1)
            self.logger.info("get login website " + self.url1)
            
            save_path = os.path.expanduser('~')     #Downloads
            save_path = os.path.join(save_path, 'Downloads')
            
            num = 'test'
            file_name = 'q' + num + '.html'
            pdffile_name = 'q' + num + '.pdf'
            complete_name = os.path.join(save_path, file_name)
            self.logger.info(complete_name)
            
            '''
            #file_object = codecs.open(complete_name, "w", "utf-8")
            #html = driver.page_source
            #file_object.write(html)
            
            save as html
            pyautogui.hotkey('ctrl', 's')
            time.sleep(1)   
            pyautogui.typewrite(file_name)
            time.sleep(1)
            pyautogui.hotkey('enter')
            time.sleep(1)   
            '''
            #save as pdf
            pyautogui.hotkey('ctrl', 'p')
            time.sleep(7)   
            pyautogui.hotkey('enter')
            time.sleep(1)
            pyautogui.typewrite(pdffile_name)
            time.sleep(1)
            pyautogui.hotkey('enter')
            
            driver.close()
            time.sleep(1)
        except Exception as e:
            errorcode = ("2 Unexpected error in runandrecord:", sys.exc_info()[0])
            self.logger.error(errorcode)
            raise 
 
def main():
    configDict = {}
    
    #logger start 
    loggerinit = debuglogger()
    appname = 'wiley'
    filename = 'debug_%s.txt' %appname
    logger1 = loggerinit.loggerstart(appname, filename)
    configDict['logger1'] = logger1
    
    logger1.info('Start')
    oasis1 = Oasis(configDict)
    oasis1.addsettings()
    oasis1.driver_init()
    oasis1.runandrecord()
    logger1.info('Complete')

if __name__ == '__main__':
    main()





