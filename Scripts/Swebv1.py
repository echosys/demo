'''
version Aug 19 

TD:

'''

import math
import sys
import datetime
import time
import platform
import os 
import traceback
import logging 
import smtplib

from time import gmtime, strftime, localtime
from string import ascii_lowercase
from itertools import product
from email.mime.text import MIMEText
from email.header    import Header

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

#from pyvirtualdisplay import Display

        
class Sweb(object):
    
    def __init__(self, config_kwargs = {}):
        """Return a Sweb object whose name is *name*.""" 
    
        self.configDict = {
            "name" : 'spider1',
            "errorcode": 0, 
            "driverpath": "deploy",
            'logger1' : 'logger'
        }
        for (config, default) in config_kwargs.items():
            self.configDict[config] = config_kwargs[config]
        
        #common constants
        self.logger = self.configDict['logger1']

        #deploy constants
        
        #script constants
        self.name = self.configDict['name']
        self.errorcode = self.configDict['errorcode']
        self.driverpath = self.configDict['driverpath']
        self.timedict = {}
        
        #selenium constants
        self.chrome_options = Options()
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-setuid-sandbox")
        #self.chrome_options.set_headless(headless=True)
        
        #chrome no alerts, pop ups
        self.prefs = {"profile.default_content_setting_values.notifications" : 2}
        self.chrome_options.add_experimental_option("prefs",self.prefs)
        
        self.emailbody = ''

    def runandrecord(self):
        print('nothing here yet')
        pass
    
    def clearCache(self, driver):
        #clear cache https://intoli.com/blog/clear-the-chrome-browser-cache/
        #https://bugs.chromium.org/p/chromedriver/issues/detail?id=583
        
        #UI way https://stackoverflow.com/questions/32970855
        self.logger.info('Clear Cache UI will open a new page! ')
        from selenium.webdriver.common.keys import Keys
        driver.get('chrome://settings/clearBrowserData')
        driver.find_element_by_xpath('//settings-ui').send_keys(Keys.ENTER)
        time.sleep(5)
                        
    def driver_init(self):
        istest = True if self.driverpath == 'test' else False
        
        #expects drive in folder wdr_c one level up
        dpwin_st1 = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__)) ), 'webdriver_c','chromedriver.exe')
        dpwin_cus1 = os.path.join(os.path.dirname(os.path.abspath(__file__)),'chromedriver.exe' )
        dpmac = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__)) ), 'webdriver_c','chromedriver')
        dplinux = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__)) ), 'webdriver_c','chromedriver')
        if platform.system() == 'Windows': 
            self.driverpath = dpwin_st1 if istest else dpwin_cus1 #deploy
        elif platform.system() == 'Darwin': 
            self.driverpath = dpmac
        elif platform.system() == 'Linux': 
            self.driverpath = dplinux
            
        self.logger.info('now using driver: ' + self.driverpath)

    def driverwait_element(self,maxsec, xpath_entry):
        #SyntaxError: non-default argument follows default argument
        myele = WebDriverWait(driver, maxsec).until(EC.presence_of_element_located(
            (By.XPATH, xpath_entry)) )
        myele = driver.find_elements_by_xpath(xpath_entry)[0].text
        return myele

    def driverwait_elementattribute(self,maxsec, xpath_entry, attributename):
        myele = WebDriverWait(driver, maxsec).until(EC.presence_of_element_located(
            (By.XPATH, xpath_entry)) )
        ifattribute = False
        try:
            myatt = driver.find_elements_by_xpath(xpath_entry)[0].get_attribute(attributename)
        except Exception as e:
            time.wait(1)
            driverwait_elementattribute(maxsec, xpath_entry, attributename)
        return myatt
    
    def getlogin(self):
        # "r+" means "and write also"
        with open("loginxinxi.txt", "r+") as fo:
            xinxi1 = fo.readline().strip()
            xinxi2 = fo.readline().strip()
        fo.close()
        xinxi1 = xinxi1 + 'g'  
        xinxi2 = xinxi2 + str(56)
        return [xinxi1, xinxi2]
    
    def setsmtp(self, configfName):
        self.recipients_emails = []
        provider = self.smtpprovider
        with open(configfName, "r+") as fo:
            user1 = fo.readline().strip()
            pw1 = fo.readline().strip()
            self.recipients_emails.append(fo.readline().strip() )
        self.smtp_user = user1 + '@gmail.com' if provider=='gmail' else user1 + '@outlook.com'
        self.smtp_key = '{}'.format(pw1)
        self.logger.info('SMTP info - {} / {}'.format(self.smtp_user, self.smtp_key) )
        self.logger.info('SMTP set - {}'.format(self.smtpprovider) )
    
    def sendemail(self,config_kwargs = {}):
        self.emailConfig = {
            'Subject' : 'Test Message From Proj Black Berry Server',
            'From': self.smtp_user,
            'To': ", ".join(self.recipients_emails),
            'Body': self.emailbody
        }
        for (config, default) in config_kwargs.items():
            self.emailConfig[config] = config_kwargs[config]
        if self.smtpprovider == 'gmail':
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)    
        else: 
            server = smtplib.SMTP('smtp.office365.com', 587)  #587 [SSL: WRONG_VERSION_NUMBER]
            server.ehlo()
            server.starttls()
        msg = MIMEText(self.emailConfig['Body'], 'plain', 'utf-8')
        msg['Subject'] = Header(self.emailConfig['Subject'], 'utf-8')
        msg['From'] = self.emailConfig['From']
        msg['To'] = self.emailConfig['To']
        self.emailstatus = 'debug:start sending emails'
        self.logger.info('From To Body{} provider'.format(self.emailConfig['Body']) )
        
        try:  
            self.logger.info('Status: Email sending initiated...')
            server.ehlo()
            self.logger.info('Attempting...')
            server.login(self.smtp_user, self.smtp_key)
            self.logger.info('Login...')
            server.sendmail(msg['From'], self.recipients_emails, msg.as_string())
            server.close()
            self.logger.info('Email sent!')
            self.emailstatus = 'email sent...'
        except:  
            self.emailstatus = 'email not sent...'
            self.logger.info('Something went wrong...')
            self.logger.info("Unexpected error:", sys.exc_info()[0])
            #raise

        
    
    #TD use time zone library, add local time, right now no Daylight saving time, OK for AZ
    def gettime(self):
        #Unix epoch time number of seconds since 1970-01-01 00:00:00 UTC
        #datetime.datetime.utcnow() returns dataobj, round to seconds 
        utctime = round(datetime.datetime.utcnow().timestamp())
        utctimems = round(datetime.datetime.utcnow().timestamp() * 1000)
        aztime = datetime.datetime.fromtimestamp(utctime)
        utcdateobj = datetime.datetime.utcnow()
        utctimestr = utcdateobj.strftime("%m/%d/%Y, %H:%M:%S") 
        
        tdelta = datetime.timedelta(hours=7) 
        azdateobj = utcdateobj - tdelta
        aztime = round(azdateobj.timestamp())
        aztimestr = azdateobj.strftime("%m/%d/%Y, %H:%M:%S") 
        
        localdateobj = datetime.datetime.now()
        localtime = round(localdateobj.timestamp())
        localtimestr = localdateobj.strftime("%m/%d/%Y, %H:%M:%S") 
        
        self.timedict = {}
        self.timedict["utcdateobj"] = utcdateobj
        self.timedict["utctimestr"] = utctimestr
        self.timedict["utctime"] = utctime
        self.timedict["utctimems"] = utctimems
        self.timedict["azdateobj"] = azdateobj
        self.timedict["aztimestr"] = aztimestr
        self.timedict["aztime"] = aztime
        
        self.timedict["localdateobj"] = azdateobj
        self.timedict["localtimestr"] = aztimestr
        self.timedict["localtime"] = aztime
        
        return self.timedict


def runbydayofmonth(spider1):
    pass
    
def runbytimeofday(spider1, hour2run): #0-24 once per day
    while 1:
        myhour = datetime.datetime.now().hour
        myminute = datetime.datetime.now().minutes
        if myhour == hour2run:
            if minutes <= 1: 
                spider1.runandrecord()
                ifrun = False
        #if during run time past hour, will not run on sche, each run <= 24hour
        time.sleep(10)
                
            
    
def runbyminsofhour(spider1):
    pass

def runbytimeinterval(spider1, secondsInt):
    isproduction = True 
    runcount = 0
    timerdict = {}
    
    tdelta = datetime.timedelta(seconds = secondsInt)
    sys.stdout.write('run every - {} '.format(tdelta) + '\n')
    while 1:
        runcount += 1
        timetilnext = datetime.timedelta(seconds = secondsInt)
        lastrunTime = spider1.gettime()["utcdateobj"]
        nextrunTime = lastrunTime + datetime.timedelta(seconds = secondsInt)
        timerdict = {'spider1':spider1, 'timetilnext':timetilnext, 'lastrunTime':lastrunTime, 'nextrunTime':nextrunTime}
        
        spider1.runandrecord()
        
        #sleep 5 sec
        [timemsg, runtimemsg] = getTimestr(timerdict)
        for i in range(secondsInt):
            time.sleep(1)
            [timemsg, runtimemsg] = getTimestr(timerdict)
            timerdict['timetilnext'] = timerdict['timetilnext'] - datetime.timedelta(seconds = 1)
            if isproduction:
                sys.stdout.write('runcount - {} '.format(runcount) )
                sys.stdout.write(runtimemsg)
                sys.stdout.write(timemsg)
                sys.stdout.flush()
                restart_line()  
                sys.stdout.flush() 
                
def getTimestr(timerdict):
    spider1 = timerdict['spider1']
    lastrunTime = timerdict['lastrunTime']
    nextrunTime = timerdict['nextrunTime']
    timetilnext = timerdict['timetilnext']
    
        
    timemsg = ('Cur UTC-{}| AZ-{}| local-{}|'
               .format(spider1.gettime()["utctimestr"], spider1.gettime()["aztimestr"], spider1.gettime()["localtimestr"]) )
    runtimemsg = ('til next {}| last run-{}| next run-{}|'
                  .format(timetilnext , lastrunTime.strftime("%m/%d/%Y, %H:%M:%S") , nextrunTime.strftime("%m/%d/%Y, %H:%M:%S") ))
    return [timemsg, runtimemsg] 
        
def restart_line():
    sys.stdout.write('\r')
    sys.stdout.flush()
    
def getProbestr(istest = False):
    #start='a', end='z', 
    length=2
    probeStr = []
    for x in range(length, length+1):
        for combo in product(ascii_lowercase, repeat=x):
            probeStr.append(''.join(combo))
    if istest: 
        #probeStr = ['za','zb']
        probeStr = probeStr[probeStr.index('pp'):]
    return probeStr    



        
def main():
    configDict= {}
    
    import iologgerv2
    from  iologgerv2 import debuglogger
    appname = 'Swebv1'
    loggerinit = debuglogger()
    filename = 'debug_%s.txt' %appname
    logger1 = loggerinit.loggerstart(appname, filename)
    configDict['logger1'] = logger1
    
    spider1 = Sweb(configDict)
    spider1.driver_init()
    print('init done')
    
    spider1.smtpprovider = 'outlook'#'gmail'
    configfName = 'smtpoutlook.txt'
    #configfName = 'smtpgmail2.txt'
    spider1.setsmtp(configfName)
    emailConfig = {
            'Subject' : 'Test Message From Project Black Berry Server',
            'Body': 'Testa dafasf\n asdfasdf'
        }
    spider1.sendemail(emailConfig)
    
    #print(getProbestr('z',2) )
    td = datetime.timedelta(days = 15, hours = 1)
    secondsInt = int(td.total_seconds())
    runbytimeinterval(spider1, secondsInt)

'''
Function Calls for testing
'''

if __name__ == '__main__':
    main()






