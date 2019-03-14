
'''
This version last modified on Nov 6, 2018

common data structure so that we can avoid circular import 
http://tinyurl.com/ycunbg9m
'''

class statusdata(object):
    def __init__(self):
        self.raw = []
        self.done = False
        self.mode = ''  #APAC EMEA AMERICAS
        self.fnfull = ''
        self.fnonly = ''
        self.wait = 2
        
    def toString(self):
        seperator = ', '
        mylist = [self.done, self.mode]
        msg = seperator.join(mylist)
        return msg
    
    def getnull(self):
        numnull = 0
        for eachrow in self.raw:
            if eachrow[1] == True: 
                numnull = numnull + 1
        
        return numnull
        
    def getnotnull(self):
        numnull = 0
        for eachrow in self.raw:
            if eachrow[1] == False: 
                numnull = numnull + 1
        
        return numnull   
    
    def getDone(self):
        numdone = 0
        for eachrow in self.raw:
            if (eachrow[1] == False) or (eachrow[1] == True): 
                numdone = numdone + 1
        
        return numdone + 1 
    


