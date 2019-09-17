'''
Aug 2 

version:
v2 
make desc2 a dictionary
use *
rename runandrecord 
get time get email get pw

v1
during cont, read dict first then add to it to complete a dict
preview all the link, store total and entry dict to json

v05
a-z 
next aa-zz  26X26
stop and continue function, write start to a file

test
after run finish reset to aa 
diffItem start with cc   not first run 
need to start with cc
'''

import Swebv1
from Swebv1 import Sweb
import dsPersonv1
from dsPersonv1 import dirPerson
from dbv1 import sqlite3db
import iologgerv2
from iologgerv2 import debuglogger

import json
import math
import sys
import datetime
import time
import platform
import os 
import traceback

from time import gmtime, strftime, localtime


import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

#from pyvirtualdisplay import Display

        
class dirweb(Sweb):
    
    def previewCheck(self):
        '''
        return entryDict
        '''
        isfirstrun = self.configDict['isfirstrun']
        isstu = self.configDict['isstu']
        iscont = self.configDict['iscont']
        logger1 = self.configDict['logger1']
        jsonfname = self.configDict['jsonfname']
        
        self.url1 = 'https://isearch.asu.edu/asu-students/'
        self.url2 = 'https://isearch.asu.edu/asu-people/'
        driver = webdriver.Chrome(self.driverpath,options=self.chrome_options) 
        self.url = self.url1 if isstu else self.url2 
        driver.get(self.url)
        logger1.info("previewCheck website " + self.url)
        time.sleep(2)
        totalentry = 0
        
        starttime = self.gettime()["utcdateobj"]
        logger1.info('Start Time UTC - %s , AZ - %s' % (self.gettime()["utctimestr"], self.gettime()["aztimestr"]))
        
        #login
        if(isstu):
            [input1, input2] = self.getlogin()
            #print([input1, input2])
            xpath_uname = '//*[@id="username"]'
            uname = driver.find_elements_by_xpath(xpath_uname)
            uname[0].send_keys(input1)
            xpath_pww= '//*[@id="password"]'
            pww = driver.find_elements_by_xpath(xpath_pww)
            pww[0].send_keys(input2)
            
            xpath_submit = '//*[@id="login_submit"]/input'
            submitb= driver.find_elements_by_xpath(xpath_submit)
            submitb[0].click()
            time.sleep(2)
                
        #pop up t&c removal
        xpath_iagree = '/html/body/div[1]/div/a[2]'
        iagree = driver.find_elements_by_xpath(xpath_iagree)
        iagree[0].click()
        time.sleep(1)
        
        diffItems = []
        if iscont: 
            [pstr, diffpstr, diffItems] = iologgerv2.readjson_prog(jsonfname)
            probeStr = Swebv1.getProbestr() #if isfirstrun else diffItems
            if diffpstr in probeStr:
                logger1.info('Diff progress record found, starting with \'%s\'' %pstr)
            else:
                diffpstr = probeStr[0]
                logger1.info('No diff progress record found, start with \'%s\'' %pstr)
            startstr = diffpstr
        #pstr should be in all str or diffItems    what if iscont diffItem do not start with aa  
        elif not iscont: 
            startstr = probeStr[0]
            
        endstr = probeStr[probeStr.index(startstr) + 3] if istest else probeStr[-1]
        startindex = probeStr.index(startstr)
        endindex = probeStr.index(endstr)
        logger1.info('firstrun?-{} isstu?-{} iscont?-{}'.format(isfirstrun, isstu, iscont) )
        logger1.info('start?:{} index?:{} endstr?:{} endindex?:{} probeStr[{}]-{}'
                     .format(startstr, startindex, endstr, endindex, len(probeStr), probeStr) )
        
        testingProbe = False #testing only 2 probe str
        probeStr = Swebv1.getProbestr(testingProbe)
        logger1.info(probeStr)

        for curkey in probeStr[startindex: endindex+1]:
        #for curkey in probeStr:
            time.sleep(2) # wait for text box old entry
            driver.get(self.url)
            
            #pop up survey page 
            xpath_nothanks = '//*[@id="acsMainInvite"]/div/a[1]'
            xpath_close = '/html/body/script[6]'
            xpath_yes = '//*[@id="acsFocusFirst"]'
            nobutton = driver.find_elements_by_xpath(xpath_nothanks)
            if len(nobutton) > 0:
                nobutton[0].click()
            
            #search field type in and enter
            xpath_searchtext = '//*[@id="edit-is-ajax-search-text"]'
            searchtext = driver.find_elements_by_xpath(xpath_searchtext)
            searchtext[0].clear()
            searchtext[0].send_keys(curkey)
            xpath_searchbutton = '//*[@id="edit-submit"]/i'
            searchbutton = driver.find_elements_by_xpath(xpath_searchbutton)
            searchbutton[0].click()
            time.sleep(3)
            
            #entry per letter
            xpath_numresults = '//*[@id="is-ajax-solr-resultcount"]/span'
            numresults = driver.find_elements_by_xpath(xpath_numresults)
            resultsfound = numresults[0].text
            logger1.info(str(resultsfound) + ' entry for %s' %curkey)
            totalentry += int(resultsfound)
            dictEntry[curkey] = int(resultsfound)
            logger1.info('Finished %s out of %s total str' %(probeStr.index(curkey)+1,  len(probeStr)) )
            logger1.info('Total entry %s' % totalentry)
            logger1.info(dictEntry)
            #now update per letter, clear diffItems as go vs in r&R
            #iologgerv2.writejson_dictonly(jsonfname, dictEntry)
            diffItems = iologgerv2.updatejson_diff(jsonfname, dictEntry)
            

        logger1.info('Finish Time UTC - %s , AZ - %s' % (self.gettime()["utctimestr"], self.gettime()["aztimestr"]))
        finishtime = self.gettime()["utcdateobj"]
        logger1.info('Time spent %s' % (finishtime-starttime) )
        
        #iologgerv2.writejson_dictonly(jsonfname, dictEntry)
        logger1.info('Total entry %s' % totalentry)
        logger1.info(dictEntry)
        
        time.sleep(1)
        driver.quit() 
        return dictEntry, diffItems
     
    def runandrecord(self):
        
        try:  
            istest = False
            
            isstu = self.configDict['isstu']
            isfirstrun = self.configDict['isfirstrun']
            iscont = self.configDict['iscont']
            jsonfname = self.configDict['jsonfname']
            mysem = self.configDict['mysem']
            logger1 = self.configDict['logger1']

            #display = Display(visible=0, size=(800, 600))
            #display.start()
            
            self.url1 = 'https://isearch.asu.edu/asu-students'
            self.url2 = 'https://isearch.asu.edu/asu-people'
            driver = webdriver.Chrome(self.driverpath,options=self.chrome_options) 
            # Ternary Operators
            self.url = self.url1 if isstu else self.url2 
            driver.get(self.url)
            logger1.info("get login website " + self.url)
            time.sleep(2) #get page 
            starttime = self.gettime()["utcdateobj"]
            logger1.info('Start Time UTC - %s , AZ - %s' % (self.gettime()["utctimestr"], self.gettime()["aztimestr"]))
            totalentry = 0
            dictEntry = {}
            
            #login
            if(isstu):
                [input1, input2] = self.getlogin()
                #print([input1, input2])
                xpath_uname = '//*[@id="username"]'
                uname = driver.find_elements_by_xpath(xpath_uname)
                uname[0].send_keys(input1)
                xpath_pww= '//*[@id="password"]'
                pww = driver.find_elements_by_xpath(xpath_pww)
                pww[0].send_keys(input2)
                
                xpath_submit = '//*[@id="login_submit"]/input'
                submitb= driver.find_elements_by_xpath(xpath_submit)
                submitb[0].click()
                time.sleep(2)
            
            #pop up removal
            xpath_iagree = '/html/body/div[1]/div/a[2]'
            iagree = driver.find_elements_by_xpath(xpath_iagree)
            iagree[0].click()
            time.sleep(1)
            
            #open DB 
            mydb = sqlite3db('dirdata.db')
            mydb.connStart(logger1)
            
            if iscont: 
                progresults = iologgerv2.readjson_prog(jsonfname)
                [pstr, diffpstr, diffItems, pagenumStart]  = progresults[0:4]
                pagenumStart = int(pagenumStart)
                if pagenumStart > 1:
                    logger1.info('Progress record found, starting with \'%s\'' %pagenumStart)
                    pint = (pagenumStart-1)*10 
                    urlpagefac = '/q=*&start={}&fq=affiliations:((Courtesy+Affiliate%20NOT%20Student)%20OR%20Employee)'.format(pint)    
                    urlpagestu = '/q=*&start={}&fq=affiliations:Student'.format(pint)
                    self.url = self.url + urlpagestu if isstu else self.url + urlpagefac
                    driver.get(self.url)
                    logger1.info('Go to page \'%s\'' %self.url)
                else:
                    pagenumStart = 1
                    urlpagefac = '/q=*&fq=affiliations:((Courtesy+Affiliate%20NOT%20Student)%20OR%20Employee)'  
                    urlpagestu = '/q=*&fq=affiliations:Student' 
                    self.url = self.url + urlpagestu if isstu else self.url + urlpagefac
                    driver.get(self.url)
                    logger1.info('No progress record found, start with \'%s\'' %pagenumStart)
            elif not iscont: 
                pass
                          
            logger1.info('firstrun?-{} isstu?-{} iscont?-{}'.format(isfirstrun, isstu, iscont) )
            logger1.info('start page:{} '
                         .format(pagenumStart) )
            time.sleep(1) # wait for text box old str clear
            
            #pop up survey page 
            xpath_nothanks = '//*[@id="acsMainInvite"]/div/a[1]'
            xpath_close = '/html/body/script[6]'
            xpath_yes = '//*[@id="acsFocusFirst"]'
            nobutton = driver.find_elements_by_xpath(xpath_nothanks)
            if len(nobutton) > 0:
                nobutton[0].click()
            
            #entry per letter
            xpath_numresults = '//*[@id="is-ajax-solr-resultcount"]/span'
            numresults = driver.find_elements_by_xpath(xpath_numresults)
            resultsfound = numresults[0].text
            logger1.info(str(resultsfound) + ' entry')
            totalentry += int(resultsfound)
            
            #entry on cur page
            xpath_numentry = '//*[@id="is-ajax-solr-results"]/div'
            numentry = driver.find_elements_by_xpath(xpath_numentry)
            nume = len(numentry)
            logger1.info('%s entry this page' %nume)
            numprocessed_curkey = 0
            
            #each page 10, total page = nume/10 round up 299/10 = 30
            pagenumEnd = pagenumStart + 2 if istest else math.ceil(int(resultsfound)/10) 
            for eachpage in range(pagenumStart, pagenumEnd): 
                time.sleep(1) # wait for next page load
                logger1.info('now crawling %s out of %s pages' %(eachpage, pagenumEnd) )  #index from start
                #update nume for last page
                numentry = driver.find_elements_by_xpath(xpath_numentry)
                nume = len(numentry)
                numprocessed_curkey += nume
                
                field = 'pint'
                value = eachpage
                iologgerv2.writejson_single(jsonfname, field, value)
            
                xpath_table = '//*[@id="is-ajax-solr-results"]'
                #each student
                for i in range(nume):
                    # xpath index start with 1
                    xpath_entry = xpath_table + '/div[{var}]'.format(var = i+1)
                    xpath_desc1 = xpath_entry + '/div[2]'
                    xpath_desc2 = xpath_entry + '/div[3]'
                    xpath_imagelink = xpath_entry + '/div[1]//img'
                    
                    #eid, name, email
                    eid = WebDriverWait(driver, 3).until(EC.presence_of_element_located(
                        (By.XPATH, xpath_entry)) )
                    eid = driver.find_elements_by_xpath(xpath_entry)[0].get_attribute('eid')
                    #element is there but attribute is not https://stackoverflow.com/questions/43813170
                    
                    desc1 = WebDriverWait(driver, 3).until(EC.presence_of_element_located(
                        (By.XPATH, xpath_desc1)) )
                    desc1 = driver.find_elements_by_xpath(xpath_desc1)[0].text
                    
                    desc2 = WebDriverWait(driver, 3).until(EC.presence_of_element_located(
                        (By.XPATH, xpath_desc2)) )
                    desc2 = driver.find_elements_by_xpath(xpath_desc2)[0].text
                    
                    #optional fields
                    imagelink = driver.find_elements_by_xpath(xpath_imagelink)
                    imagelink = imagelink[0].get_attribute('src') if len(imagelink) > 0 else ''
                    
                    logger1.info(eid)
                    logger1.debug(repr(desc1) )
                    logger1.debug(repr(desc2) )
                    logger1.debug(imagelink)
                
                    #to DS                        
                    #record time for the run 
                    utctime = self.gettime()["utctime"]
                    utctimestr = self.gettime()["utctimestr"]
                    utctimems = self.gettime()["utctimems"]
                    
                    myP = dirPerson(logger1)
                    myP.desc1 = desc1
                    myP.desc2 = desc2
                    myP.email = desc2.split('\n')[0]
                    myP.name = desc1.split('\n')[0]
                    myP.semester = [mysem]
                    myP.eid = eid
                    myP.imglink = imagelink
                    myP.weblink = ''
                    
                    myP.updateTime = utctime
                    myP.updateTimestr = utctimestr
                    myP.insertTime = utctime
                    myP.insertTimestr = utctimestr
                    myP.oldInfo1 = ''
                    myP.oldInfo2 = ''
                    # can be faculty and student
                    myP.isfaculty = ['faculty'] if not isstu else ['stu']
                    #myP.isstu = ['stu'] if isstu else [] 
                    #print(myP.toString() )
                    newlist = myP.toList()
                    
                    #to DB 
                    ifexist = mydb.ifexist(myP)
                    if ifexist: 
                        oldlist = mydb.read_row(myP)
                        oldP = dsPersonv1.list2obj(oldlist, logger1)
                        result_compare= myP.compare(oldP, utctimems, utctimestr)
                        #[ifupdate, newmyP, timestamp, changetype, oldP.eid, changeditems, dictOld_str, dictNew_str]
                        if result_compare[0]:
                            mydb.update_row(result_compare[1])
                            mydb.create_log(result_compare[2:])
                            #In list[first:last], last is not included
                            
                            whichtable = (myP.isfaculty == ['stu'])
                            mydb.update_row_stufac(result_compare[1], whichtable)
                    else: 
                        mydb.create_row(myP)
                        if not isfirstrun: 
                            #if it is not first run, this is a new person, add to change log 
                            myDict = dsPersonv1.obj2dict(myP)
                            result_compare = [False, myP, utctimems, utctimestr, 'new', myP.eid, list(myDict.keys()),'',json.dumps(myDict)]
                            mydb.create_log(result_compare[2:])
                            
                        whichtable = (myP.isfaculty == ['stu'])
                        mydb.create_row_stufac(myP, whichtable)
        
                xpath_nextbutton = '//*[@class="pager-next"]' #'//*[@class="asu-dir-hidden"]' #pres and next
                #if nume == 10: #even pages 20 entry breaks, if done<total, next page 
                if numprocessed_curkey < int(resultsfound):
                    #StaleElementReferenceException
                    #nextbutton = driver.find_elements_by_xpath(xpath_nextbutton)
                    #nextbutton[0].click()   hidden element can not click  
                    nextbutton = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.XPATH, xpath_nextbutton))
                    )
                    nextbutton = driver.find_elements_by_xpath(xpath_nextbutton)
                    webdriver.ActionChains(driver).move_to_element(nextbutton[0]).click().perform()

                logger1.info('finished %s out of %s pages' %(eachpage, pagenumEnd) ) 
                time.sleep(0.2)   
                entrydone = numprocessed_curkey + eachpage*10
                logger1.info('finished %s out of %s entries' %(entrydone, resultsfound) ) 
                '''
                #each letter
                #driver.quit() #close driver, clear cache
                logger1.info(dictEntry)
                logger1.info(thisentry)
                iologgerv2.updatejson_dictonly(jsonfname, thisentry)
                '''
                
            mydb.connClose()
            logger1.info('Finish Time UTC - %s , AZ - %s' % (self.gettime()["utctimestr"], self.gettime()["aztimestr"]))
            finishtime = self.gettime()["utcdateobj"]
            logger1.info('Time spent %s' % (finishtime-starttime) )
            
            #logger1.info('Total entry %s' % totalentry)
            #logger1.info(dictEntry)
            
            #now update each letter rather than overwrite after done
            #iologgerv2.writejson_dictonly(jsonfname, dictEntry)
            #iologgerv2.writejson_prog(jsonfname, 'aa')
            logger1.info('Finished json dictEntry and reset progress')
            
            #close driver
            time.sleep(5)
            #driver.close()  #close window on focus
            driver.quit()
            #isplay.stop()
            time.sleep(1)

                    
        except NoSuchElementException as e:
            logger1.error(e)
            logger1.error('try again next time...')
            
            time.sleep(1)
            try: 
                #driver.quit()
                #display.stop()
                pass
            except:
                logger1.error("Unexpected error:", sys.exc_info()[0])
                logger1.error("-----Detail:", sys.exc_info()[1])
        
        except:
            try: 
                #driver.quit()
                #display.stop()
                pass
            except:
                logger1.error("Unexpected error:", sys.exc_info()[0])
                logger1.error("-----Detail:", sys.exc_info()[1])
                
            var = traceback.format_exc().splitlines()
            if len(var)>30: var = var[:-30]    
            msgerror = "Unexpected error:" + str(sys.exc_info()[0])
            msgdetail = "-----Detail:" + '\n'.join(var )
            logger1.error(msgerror)
            logger1.error('\n'.join(var ))
            raise  #re-raise the exception (allowing a caller to handle the exception as well)


def main():  
    #faculty then student/ 19Sum1 First run True/
    configDict = {}
    configDict['name'] = 'spider1'
    configDict['mysem'] = '19Sum1'  
    configDict['isfirstrun'] = True    #diffItems of allstr
    configDict['iscont'] = True         #pstr or allstr/dItem[0]
    configDict['isstu'] = False
    configDict['driverpath'] = 'deploy' #test or deploy
    
    #logger start 
    loggerinit = debuglogger()
    appname = configDict['mysem']
    filename = 'debug_%s.txt' %appname
    logger1 = loggerinit.loggerstart(appname, filename)
    configDict['logger1'] = logger1
    
    isfirstrun = configDict['isfirstrun']
    isstu = configDict['isstu']
    iscont = configDict['iscont']
    
    spider1 = dirweb(configDict)
    spider1.driver_init()
    
    if isstu:
        spider1.configDict['jsonfname'] = 'dirSum_p1_stu.json'
        #entryDict_new = spider1.previewCheck()
    else: 
        spider1.configDict['jsonfname'] = 'dirSum_p1_fac.json'
        #entryDict_new = spider1.previewCheck()
    
    #if firstrun, allstr vs diffItems / if cont pstr vs 'aa'
    if isfirstrun:
        logger1.info('firstrun?-{} isstu?-{} iscont?-{}'.format(isfirstrun, isstu, iscont) )
        spider1.runandrecord()
    elif not isfirstrun:   
        # if iscont do not check preview each time, cont based on diff items 
        if not iscont:
            entryDict_new, diffItems = spider1.previewCheck()
            #now diff as preview run
            #diffItems = writejson_diff(spider1.configDict['jsonfname'], entryDict_new)
        if len(diffItems) > 0:
            logger1.info('firstrun?-{} isstu?-{} iscont?-{} diffItems-{}'.format(isfirstrun, isstu, iscont, diffItems) )
            spider1.runandrecord()
        else: 
            #no change since last run
            logger1.info('no change since last run')
    

    print('init_run1 done')

'''
Function Calls
'''
if __name__ == '__main__':
    main()






