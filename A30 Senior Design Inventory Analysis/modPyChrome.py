'''
Created on Oct 19, 2018

@author: Jean_Claude
'''

import os 
import re 
import time
import PyChromeDevTools

from bs4 import BeautifulSoup

import modDSv1

class PyChrome(object):
    def __init__(self, statusdata):
        '''
        Constructor
        '''
        # instance method
        self.data = statusdata
        self.chrome = None 
        self.mainurl = None

    def runMain(self):
        self.americasmain = "https://www.avnet.com/wps/portal/us/"
        self.apacmain = "https://www.avnet.com/wps/portal/apac/"
        self.emeamain = "https://www.avnet.com/wps/portal/emea/"
        self.mainurl = "https://www.avnet.com/"
        
        if (self.data.mode == "AMERICAS"):
            self.mainurl = self.americasmain
        elif (self.data.mode == "APAC"):
            self.mainurl = self.apacmain
        elif (self.data.mode == "EMEA"):
            self.mainurl = self.emeamain  
        else:
            self.mainurl = self.americasmain
        
        ua = "Google Chrome Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        
        chrome = PyChromeDevTools.ChromeInterface()
        self.chrome = chrome
        chrome.Network.enable()
        chrome.Network.setUserAgentOverride(userAgent = ua)
        
        chrome.Page.navigate(url = self.mainurl)
        self.data.logger.info('Get page {}'.format(self.mainurl))
        time.sleep(5)
        return chrome
        
    
    def checkNull(self, chrome, eachrow):
        entry = eachrow[0]
        url_lhs = 'https://www.avnet.com/shop/SearchDisplay?searchTerm='
        url_lhs = 'https://www.avnet.com/shop/us/search/'
        url_rhs = entry
        
        #check Avnet first
        chrome.Page.navigate(url = self.mainurl)
        time.sleep(self.data.wait)
        chrome.Page.navigate(url = url_lhs + url_rhs)
        mydom = chrome.DOM.getDocument(-1)  #-1 get all nodes
        
        try: 
            soup = BeautifulSoup(mydom) 
            print(soup.original_encoding)   
        except Exception as e:
            continue
        
        his = chrome.Page.getNavigationHistory()
        #self.data.logger.info(his)
        his_last = his['result']['entries'][-1]['url']
        self.data.logger.info(his_last)
        '''
        #use redirect url to check if there is stock available
        #ER412DM4-26A/SQ  vs       #https://www.avnet.com/shop/NoSearchResultsView?noResultTerm=asdfdsafasdf&storeId=      
        We couldn't find any products for "﻿INTERNAL SEARCH TERM"
        https://www.avnet.com/shop/us/search/k4b2g1646q-bck0
        https://www.avnet.com/shop/SearchDisplay?searchTerm=K4B2G1646Q-BCK0
        
        We weren't able to find any results based on your search entry.
        https://www.digikey.com/products/en?keywords=
        '''
        if "NoSearchResultsView" in his_last: 
            eachrow[1] = True 
        #elif xpath $x('/html/body/h1')[0].textContent  contains Generic Application Error
        else:
            eachrow[1] = False
        self.data.logger.info(eachrow)
        
        #arrow always shows stock, nearest result
        #check digikey next 
        
        #now clear cache each sec to avoid Generic Application Error
        chrome.Network.clearBrowserCache()
        chrome.Network.clearBrowserCookies()
        return eachrow
    
    def runandRecord(self):
        self.runMain()
        for key, value in self.data.dataDict.items():
            eachrow = [key, value[0], value[1]]
            eachrow = self.checkNull(self.chrome, eachrow)
            self.data.dataDict[key] = [eachrow[1], eachrow[2]]
            print(eachrow)
        self.data.done = True
        
    def checknullall(self):
        self.chrome = self.initrun()
        for index, eachrow in enumerate(self.data.raw):
            if (index != 0):
                if (eachrow[1] == True or eachrow[1] == False):   #for resume feature
                    pass
                else:
                    eachrow = self.checknull(eachrow, self.chrome)
                    print(eachrow)
                    print(self.data.raw)
        self.data.done = True
        

if __name__ == '__main__':

    test1 = ['DS28C22Q+U', '']
    test2 = ['asdfsadfaf', '']
    
    mystatusdata = modDSv1.statusdata()
    mystatusdata.raw = [['DS28C22Q+U', ''], ['asdfsadfaf', '']]
    mystatusdata.mode = "APAC"
    mikey = PyChrome(mystatusdata)
    mikey.checknullall()


