
'''
This version last modified on Sep 9 2017

Version Notes: 
v3:
visit piazza 355/ 380/301, login to piaza and visit Q&A pages
visit top half posts each 

Deploy Notes
v3 does not check if the advertisement is present, will thrown a index out of range error
log file for tracking valid logins

Enhancements

Version History


'''

#deploy
#from pyvirtualdisplay import Display

import smtplib
import os
from time import gmtime, strftime, localtime, time
import sys
import time
import datetime
import collections

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import UnexpectedAlertPresentException

import Swebv1
from Swebv1 import Sweb
import iologgerv2
from  iologgerv2 import debuglogger

actnum = 1;
    
    
class Fbweb(Sweb):
    
    def chromedriverrun(self):
        """Return a Fbweb object whose name is *name*.""" 
        #selenium constants
        self.listlocation = 6

        self.url1 = "https://piazza.com/class/j6fyaicyxrvwh" #355
        self.url1_1 = "https://piazza.com/class/j5l9qym2w2i2yg" #380
        self.url1_2 = "https://piazza.com/class/j6hcr2wdz8a28b" #301
        self.url2 = "https://piazza.com/class/j6fyaicyxrvwh?cid="
        self.login = "lingtaog@asu.edu"
        self.pwpw = "qwer1570"
        self.urllist = [self.url1]

    def runandrecord(self):
        self.chromedriverrun()
        self.driverstart()
        
    def driverstart(self):
        try:    
            #display = Display(visible=0, size=(800, 600))
            #display.start()
            driver = webdriver.Chrome(self.driverpath,options=self.chrome_options)
            driver.get(self.url1)
            self.logger.info("get login website " + self.url1)
            
            driver.implicitly_wait(1)
            #may be explicit wait, sometimes not finding the submit button
            input1 = driver.find_element(By.NAME, "email").send_keys(self.login)
            input2 = driver.find_element(By.NAME, "password").send_keys(self.pwpw)
            driver.implicitly_wait(1)
            loginbutton3 = driver.find_element_by_xpath("//button[@id = 'modal_login_button']").click()
            
            for eachurl in self.urllist:
                try:
                    driver.implicitly_wait(1)
                    driver.get(eachurl)
                except UnexpectedAlertPresentException as e:
                    alert = driver.switch_to.alert
                    alert.dismiss()
                    time.sleep(1)
                    self.logger.error("failed to get to website " + eachurl)
                    driver.get(eachurl)
                if isAlertPresent(driver):
                    alert = driver.switch_to.alert
                    alert.dismiss()
                time.sleep(1)
                
            self.readposts(driver)
            #close driver
            driver.quit()
            #display.stop()
        
                    
        except NoSuchElementException as e:
            self.logger.error(e)
            self.logger.error('try again next time...')
            
            time.sleep(1)
            driver.quit()
            #display.stop()
            
        except UnexpectedAlertPresentException as e:
            alert = driver.switch_to.alert
            alert.dismiss()
            time.sleep(1)
            self.logger.error('UnexpectedAlertPresentException...')
            driver.quit()
            #display.stop()
        
        except:
            self.logger.error("Print Unexpected error:", sys.exc_info()[0])
            raise
    
    def readposts(self, driver):
        for eachurl in self.urllist:
            #driver.implicitly_wait(1)
            time.sleep(2)
            driver.get(eachurl)
            #driver.execute_script("window.scrollTo(0, 1000);")
            self.Introall1 = driver.find_elements_by_xpath("//span[@id = 'total_posts_count']")
    
            self.logger.info('number of elements found: ' + str(len(self.Introall1)))
            self.logger.info('number of posts found: ' +  self.Introall1[0].text )
            posts = int(self.Introall1[0].text)
            
            for i in range (posts, int(posts/2), -1):
            #for i in range (posts, posts-5, -1):
                curposturl = eachurl + "?cid=" + str(i)
                try:
                    driver.get(curposturl)
                except UnexpectedAlertPresentException as e:
                    alert = driver.switch_to.alert
                    alert.dismiss()
                    time.sleep(1)
                if isAlertPresent(driver):
                    alert = driver.switch_to.alert
                    alert.dismiss()
                if (i%2 == 0):
                    self.logger.info("get info website " + curposturl)
                time.sleep(1)
                driver.implicitly_wait(1)
                
def isAlertPresent(driver): 
    try: 
        driver.switch_to.alert
    except NoAlertPresentException as e:
        return False; 
            

def main():
    #schedule every 5 hour
    configDict = {}
    configDict['appname'] = 'pjpiaza'
    configDict['jsonfname'] = 'pjpiaza.txt'
    appname = configDict['appname']

    #logger start 
    loggerinit = debuglogger()
    filename = 'debug_%s.txt' %appname
    logger1 = loggerinit.loggerstart(appname, filename)
    configDict['logger1'] = logger1

    configDict['driverpath'] = 'depoly'
    
    spider1 = Fbweb(configDict)
    spider1.driver_init()
        
    td = datetime.timedelta(minutes = 15)
    secondsInt = int(td.total_seconds())
    Swebv1.runbytimeinterval(spider1, secondsInt)    

'''
Function Calls
'''
if __name__ == '__main__':
    main()






