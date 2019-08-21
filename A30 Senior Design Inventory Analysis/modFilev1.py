'''
Created on Oct 19, 2018

@author: Jean_Claude
'''
import datetime
import csv

import modDSv1


class Filehandler(object):

    def __init__(self, statusdata):
        '''
        Constructor
        '''
        # instance method
        self.data = statusdata
        
        self.filepath = self.data.filepath
        self.fnonly = self.data.fnonly
        
        statusdata.dataDict = {}
    
    def readCsv_asdict(self):
        mode = 'r+'
        self.data.logger.info('opening csv {}'.format(self.data.filepath) )
        with open(self.data.filepath, encoding="utf8") as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            rownum = 0
            for row in spamreader: #row here is list ['\ufeffInternal Search Term', 'Null?']
                rownum += 1
                if len(row) == 2 and rownum > 1:
                    [item, ifnullonAvnet] = row
                else: 
                    item = row[0]
                    ifnullonAvnet = 'ifnullonAvnet'
                item = item[:30]  #limit to 30 char 
                self.data.dataDict[item] = [ifnullonAvnet, 'ifnullonArrow']
    
    def writeJson_fromdict(self):
        pass
                
    def writeCsv_fromdict(self):
        pass
    
    def readCsv_aslist(self):
        mode = 'w'
        with open(self.filename, encoding="utf8") as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in spamreader:
                self.data.raw.append(row)
                #print(row)
        #print(self.data.raw)
        #[['\xef\xbb\xbfInternal Search Term', 'Null?'], ['DS28C22Q+U', ''], ['AES-MMP-7K410T-G', '']
    
    def writeCsv_fromlist(self):
        timestamp = datetime.datetime.now().strftime("%I-%M-%S-%p-%B-%d-%Y")    #'10-36-01-AM-July-23-2010'
        outfile = self.fnonly + "_DONE_"+ timestamp + ".csv"
        self.csvcontent = self.data.raw
        
        with open(outfile, 'w', newline='',encoding="utf8") as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for row in self.csvcontent:
                spamwriter.writerow(row)
    
    
    
if __name__ == '__main__':
    mydata = modDSv1.statusdata()
    mikey = CSVhandler(mydata)
    
    # call our instance methods
    filename =  'AMERICAS Nulls.csv'
    mikey.readcsv(filename)
    
    mikey.writecsv()
     