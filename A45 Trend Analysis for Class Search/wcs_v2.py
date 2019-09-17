'''
This version last modified on Nov 6, 2018

TD:
need to close last driver if error occurs 
try close driver with in catch phrase

add relative path for deployment driver 
add options to change user agent and clear cache, cookie

need to add sys call to bat file each run and clean up process after drive.quit()
'''


import sys
import datetime
import time
from time import gmtime, strftime, localtime
import platform
import os 
import traceback


import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

#from pyvirtualdisplay import Display
import fileiov2         #when testing fileiov2, we import wcs_v2, and have to comment this one out, import also calls main
import smtp_gmv1
from dsv1 import cse
        
class Fbweb(object):
    
    def __init__(self, name, dp):
        """Return a Fbweb object whose name is *name*.""" 
        #selenium constants
        self.name = name
        self.logger = None
        
        #output constants

        #deploy constants
        self.time2runlist = [7, 17, 25, 35, 47, 55]
        #script constants
        self.utcstr = 'init time'
        self.aztimestr = 'init az time'
        self.errorcode = 'init errorcode'
        self.driverpath = dp

        self.chrome_options = Options()
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-setuid-sandbox")
        self.chrome_options.set_headless(headless=True)
        
        #chrome no alerts, pop ups
        self.prefs = {"profile.default_content_setting_values.notifications" : 2}
        self.chrome_options.add_experimental_option("prefs",self.prefs)

    def runandrecord(self):
        #os.system("taskkill /f /im chrome.exe")   #careful, this closes all chrome instance
        time.sleep(3)         #some data processing needs chrome elements, kill before new run
        
        try:    
            self.errorcode = None
            #display = Display(visible=0, size=(800, 600))
            #display.start()
            
            self.url1 = 'https://webapp4.asu.edu/catalog/classlist?t=2191&s=CSE&n=5*&hon=F&promod=F&e=all&page=1'
            driver = webdriver.Chrome(self.driverpath,options=self.chrome_options) 
            driver.get(self.url1)
            print("get login website " + self.url1)
            
            time.sleep(3) # Let the user actually see something!
            
            #expr = "//*[matches(@id, 'informal(_)?([0-9])?')]"   #The string is not a valid XPath expression.
            expr = "//*[starts-with(@id,'informal')]"
            rows = driver.find_elements_by_xpath(expr)
            print(len(rows) )
            objlist = []
            printlist = []
            
            for row in rows: 
                print('        '+row.get_attribute("class") + row.get_attribute("id"))
                #.findElements(By.xpath(".//*"));
                cnum = row.find_element_by_xpath(".//td[1]").text
                ctitle = row.find_element_by_xpath(".//td[2]/div").text
                cregnum = row.find_element_by_xpath(".//td[3]/a").text          #the heck xpath is 1 based
                
                cseatsopen = row.find_element_by_xpath(".//div/div[1]").text
                cseatstotal = row.find_element_by_xpath(".//div/div[3]").text
                cindicator = row.find_element_by_xpath(".//div/div/span/span/i").get_attribute("title")
                #seats reserved #seats unavailable #seats available
                print(cnum, ctitle, cregnum, cseatsopen, cseatstotal, cindicator)
                cseclass = cse()
                cseclass.cnum = cnum
                cseclass.ctitle = ctitle
                cseclass.cregnum = cregnum
                cseclass.cseatsopen = cseatsopen
                cseclass.cseatstotal = cseatstotal
                cseclass.cindicator = cindicator
                objlist.append(cseclass)
                class2text = cseclass.cnum +','+ cseclass.ctitle +','+ cseclass.cregnum +',' +cseclass.cseatsopen +','+ cseclass.cseatstotal +','+ cseclass.cindicator
                printlist.append(class2text)
                cseclass = cse()
                
            #order of operation, read from cur, write to past, write to cur, add to log
            datalast = []
            datalast = fileiov2.txt2list(datalast, "datacur.txt")
            #print(datalast)
            fileiov2.list2txt(datalast, "datapast.txt")
            
            fileiov2.list2txt(printlist, "datacur.txt")
            fileiov2.logtxt(printlist, "datalog.txt")
            
            objcur = objlist
            objlast =  fileiov2.list2obj(datalast)
            printlist = fileiov2.datacompare(objcur, objlast) #datacompare cur last
            if len(printlist) > 0:
                msg = 'http://tinyurl.com/y755okux'
                for eachprintstruct in printlist:
                    msg = msg + "\n" + eachprintstruct.toString()
                
                mygmail = smtp_gmv1.smtpgmail()
                mygmail.sendonce(['gelingtao@gmail.com'], msg)
                #mygmail.sendonce(['yuxuezhou.9712@gmail.com'], msg)
                
                self.logger.dladd(msg)
            else:
#                 msg = "mygmail.sendonce(['gelingtao@gmail.com'], msg)"
#                 mygmail = smtp_gmv1.smtpgmail()
#                 mygmail.sendonce(['gelingtao@gmail.com'], msg)
                print("nothing has changed this run")   
                print(fileiov2.gettime()) 
                self.logger.dladd('successful run with no change')
            """Datalog.txt  all data/ server_log changed data"""
            

            #close driver
            time.sleep(3)
            driver.close()
            driver.quit()
            #isplay.stop()
            time.sleep(1)

                    
        except NoSuchElementException as e:
            print(e)
            print('try again next time...')
            
            time.sleep(1)
            try: 
                driver.quit()
                #display.stop()
            except:
                print("Unexpected error:", sys.exc_info()[0])
                print("-----Detail:", sys.exc_info()[1])
        
        except:
            try: 
                driver.quit()
                #display.stop()
            except:
                print("Unexpected error:", sys.exc_info()[0])
                print("-----Detail:", sys.exc_info()[1])
                
            var = traceback.format_exc().splitlines()
            if len(var)>30: var = var[:-30]    
            msgerror = "Unexpected error:" + str(sys.exc_info()[0])
            msgdetail = "-----Detail:" + '\n'.join(var )
            print(msgerror)
            print('\n'.join(var ))
            self.logger.dladd(msgerror)
            self.logger.dladd(msgdetail)
            #raise  #re-raise the exception (allowing a caller to handle the exception as well)

def main_init():
    dpwin_st1 = 'G:\GitHub\Pythonprep\webdriver_c\chromedriver_win32\chromedriver.exe'
    dpwin_cus1 = os.path.dirname(os.path.abspath(__file__)) + '\\chromedriver.exe'
    dpmac = '/Users/wge/Github/Pythonprep/webdriver_c/chromedriver_mac/chromedriver'
    dplinux = ''
    driverpath = ''
    if platform.system() == 'Windows': 
        #driverpath = dpwin_st1
        driverpath = dpwin_cus1 #deployment
    elif platform.system() == 'Darwin': 
        driverpath = dpmac
    elif platform.system() == 'Linux': 
        driverpath = dplinux
        
    spider1 = Fbweb('spider1', driverpath)
    spider1.logger = fileiov2.debuglogger()
    spider1.logger.debugloggerstart()
    return spider1

def main_loop(spider1):
    spider1.runandrecord()

def main():
    spider1 = main_init()
    main_loop(spider1)
    print('init_run1 done')

    while 1:
        time.sleep(5)
        main_loop(spider1)

'''
Function Calls
'''
main()







