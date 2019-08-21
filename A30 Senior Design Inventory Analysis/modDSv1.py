
'''
This version last modified on Nov 6, 2018

Class to pass status, logger around 
'''

class statusdata(object):
    def __init__(self):
        self.raw = []
        self.done = False
        self.mode = ''  #APAC EMEA AMERICAS
        self.filepath = ''
        self.fnonly = ''
        self.wait = 2
        self.logger = ''
        
        self.dataDict = {}
        
    def toString(self):
        seperator = ', '
        mylist = [self.done, self.mode]
        msg = seperator.join(mylist)
        return msg
    
    def getStatus_fromdict(self):
        statusDict = {}
        numnull_avnet, numavail_avnet, numnull_arrow, numavail_arrow, numdone = (0,)*5
        numtotal = len(self.dataDict.items())
        for eachitem in self.dataDict.items():
            (key, value) = eachitem 
            if value[0] == True or value[0] == False:
                numdone += 1
                
            if value[0] == True: 
                numnull_avnet = numnull_avnet + 1
            elif value[0] == False: 
                numavail_avnet = numavail_avnet + 1
            elif value[1] == True: 
                numnull_arrow = numnull_arrow + 1
            elif value[1] == False: 
                numavail_arrow = numavail_arrow + 1
        statusDict = {'numnull_avnet': numnull_avnet, 'numavail_avnet': numavail_avnet, 'numnull_arrow': numnull_arrow,
                      'numavail_arrow': numavail_arrow, 'numtotal': numtotal, 'numdone': numdone}
        #self.logger.info('numdone {}'.format(numdone) )
        return statusDict
        
    
    def getnull_fromlist(self):
        numnull = 0
        for eachrow in self.raw:
            if eachrow[1] == True: 
                numnull = numnull + 1
        return numnull
        
    def getnotnull_fromlist(self):
        numnull = 0
        for eachrow in self.raw:
            if eachrow[1] == False: 
                numnull = numnull + 1
        return numnull   
    
    def getDone_fromlist(self):
        numdone = 0
        for eachrow in self.raw:
            if (eachrow[1] == False) or (eachrow[1] == True): 
                numdone = numdone + 1
        return numdone + 1 
    

if __name__ == '__main__':
    pass
