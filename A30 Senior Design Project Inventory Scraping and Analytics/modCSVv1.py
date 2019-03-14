'''
Created on Oct 19, 2018

@author: Jean_Claude
'''
import datetime
import csv

import modDSv1


class CSVhandler(object):

    def __init__(self, statusdata):
        '''
        Constructor
        '''
        # instance method
        self.data = statusdata
        self.filename = self.data.fnfull
        self.fnonly = self.data.fnonly
    
    def readcsv(self):
        self.filename = self.data.fnfull
        mode = 'w'
        with open(self.filename, encoding="utf8") as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in spamreader:
                self.data.raw.append(row)
                #print(row)
        print(self.data.raw)
        #[['\xef\xbb\xbfInternal Search Term', 'Null?'], ['DS28C22Q+U', ''], ['AES-MMP-7K410T-G', '']
    
    def writecsv(self):
        self.fnonly = self.data.fnonly
        timestamp = datetime.datetime.now().strftime("%I-%M-%S-%p-%B-%d-%Y")    #'10-36-01-AM-July-23-2010'
        outfile = self.fnonly + "_DONE_"+ timestamp + ".csv"
        self.csvcontent = self.data.raw
        
        with open(outfile, 'w', newline='',encoding="utf8") as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for row in self.csvcontent:
                spamwriter.writerow(row)
    
    
    
"""
    main function 

"""    

"""  
# Instantiate the Dog object
mydata = modDSv1.statusdata()

mikey = CSVhandler(mydata)

# call our instance methods
filename =  'AMERICAS Nulls.csv'
mikey.readcsv(filename)

mikey.writecsv()
"""  