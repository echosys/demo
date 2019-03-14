'''
Created on Oct 19, 2018

@author: Jean_Claude
'''

import os 
import re 
import time
import PyChromeDevTools

import modDSv1

class PyChrome(object):
    '''
    classdocs
    '''

    def __init__(self, statusdata):
        '''
        Constructor
        '''
        # instance method
        self.data = statusdata
        self.americasmain = "https://www.avnet.com/wps/portal/us/"
        self.apacmain = "https://www.avnet.com/wps/portal/apac/"
        self.emeamain = "https://www.avnet.com/wps/portal/emea/"
        self.chrome = None 
        self.mainurl = None
        
        
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
        
    def initrun(self):
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
        chrome.Network.enable()
        chrome.Network.setUserAgentOverride(userAgent = ua)
        
        chrome.Page.navigate(url = self.mainurl)
        time.sleep(5)
        return chrome
        
    
    def checknull(self, eachrow, chrome):
        entry = eachrow[0]
        url_lhs = 'https://www.avnet.com/shop/SearchDisplay?searchTerm='
        url_rhs = entry
        
        chrome.Page.navigate(url = self.mainurl)
        time.sleep(self.data.wait)
        chrome.Page.navigate(url = url_lhs + url_rhs)
        #dom = chrome.DOM.getDocument()
        #print(dom)
        his = chrome.Page.getNavigationHistory()
        #print(his)
        #print(his['result']['entries'][-1])
        his_last = his['result']['entries'][-1]['url']
        print(his_last)
        #ER412DM4-26A/SQ
        #https://www.avnet.com/shop/NoSearchResultsView?noResultTerm=asdfdsafasdf&storeId=         
        if "NoSearchResultsView" in his_last: 
            eachrow[1] = True 
        else:
            eachrow[1] = False
        print(eachrow[1])
        
        #now clear all records 
        chrome.Network.clearBrowserCache()
        chrome.Network.clearBrowserCookies()
        
        return eachrow

        

"""
main function
comment out after testing, will call main if imported to other module
"""    

"""
test1 = ['DS28C22Q+U', '']
test2 = ['asdfsadfaf', '']

mystatusdata = modDSv1.statusdata()
mystatusdata.raw = [['DS28C22Q+U', ''], ['asdfsadfaf', '']]
mystatusdata.mode = "APAC"
mikey = PyChrome(mystatusdata)
mikey.checknullall()
"""

