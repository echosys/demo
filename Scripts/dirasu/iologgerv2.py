
'''
This version last modified on 


'''

import datetime
from time import gmtime, strftime, localtime
import sys
import logging
import json

'''
iohelper 
logger 
    logandprint
    logt1
    logt2
    lograw
    
data to string done in DS 
email from str done in email
'''

'''
standard IO helper function
'''

def jsoninit(pstr, filename, entryDict):
    total = sum([int(i) for i in entryDict.values()] )
    
    jsondata = {}
    jsondata['progress'] = []
    jsondata['progress'].append({
        'pstr': pstr,
        'diffItems': ''
    })
    jsondata['lastRun'] = []
    jsondata['lastRun'].append({
        'entryDict': entryDict, 
        'total': total
    })
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(jsondata, json_file, ensure_ascii=False, indent=4)

def readjson_prog(filename):
    with open(filename, 'r', encoding='utf-8') as json_file:
        jsondata = json.load(json_file)
        pstr = jsondata['progress'][0]['pstr']
        diffItems = jsondata['progress'][0]['diffItems']
    return pstr, diffItems

def writejson_dictonly(filename, entryDict_new): #diff writes diff and dict
    with open(filename, 'r+', encoding='utf-8') as json_file:
        jsondata = json.load(json_file)
        total_new = sum([int(i) for i in entryDict_new.values()] )
        jsondata['lastRun'][0]['entryDict'] = entryDict_new
        jsondata['lastRun'][0]['total'] = total_new
        json_file.seek(0) #overwrites
        json_file.truncate() # this deletes file content, diff Item length may vary
        json.dump(jsondata, json_file, ensure_ascii=False, indent=4)

def writejson_prog(filename, pstr):
    with open(filename, 'r+', encoding='utf-8') as json_file:
        jsondata = json.load(json_file)
        jsondata['progress'][0]['pstr'] = pstr
        json_file.seek(0) #overwrites
        json_file.truncate() # this deletes file content, diff Item length may vary
        json.dump(jsondata, json_file, ensure_ascii=False, indent=4)

def writejson_diff(filename, entryDict_new):
    with open(filename, 'r+', encoding='utf-8') as json_file:
        jsondata = json.load(json_file)
        jsondata['progress'][0]['pstr'] = pstr
        entryDict_old = jsondata['lastRun'][0]['entryDict']
        total_old = jsondata['lastRun'][0]['total']
        total_new = sum([int(i) for i in entryDict_new.values()] )
        jsondata['lastRun'][0]['entryDict'] = entryDict_new
        jsondata['lastRun'][0]['total'] = total_new
        #edge case total could be same but dict different
        diffItems = dictCompare(entryDict_new, entryDict_old)
        jsondata['progress'][0]['diffItems'] = diffItems
        
        json_file.seek(0) #overwrites
        json_file.truncate() # this deletes file content, diff Item length may vary
        json.dump(jsondata, json_file, ensure_ascii=False, indent=4)
    return diffItems

def writeprogress(pstr, filename): 
    #overwrite a progress str to txt
    with open(filename, "w") as f:
        f.write("%s" % pstr)
    
def readprogress(filename): 
    #read a progress str
    with open(filename, "r+") as f:
        pstr = f.readline()
    return pstr 
    
def list2txt(array, filename): 
    #append list 2 txt
    with open(filename, "r+") as f:
        for row in array:
            f.write(row + "\n")
    
    f.close()

def txt2list(array, filename): 
    #read txt as list
    with open(filename, "r+") as f:
        array  = f.readlines()
        array  = [x.strip() for x in array ]
    
    f.close()
    return array 

'''
error log
    can handle multithread, can handle multiple file/module write

'''
class debuglogger(object):
    def __init__(self):
        self.logger = None
    
    def loggerstart(self,appname='myservice', filename='debug_log.txt'):
        # create logger with anme appname
        self.logger = logging.getLogger(appname)
        #the logger ignore lvl lower     notset debug info warning error critical
        self.logger.setLevel(logging.DEBUG)
        # create file handler writes INFO messages or higher to the sys.stderr 
        myfh = logging.FileHandler(filename)
        myfh.setLevel(logging.DEBUG)
        #create console handler with a higher log level
        myconsole = logging.StreamHandler()
        myconsole.setLevel(logging.INFO)
        # create formatter and add it to the handlers
        formatter1 = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        myfh.setFormatter(formatter1)
        formatter2 = logging.Formatter('%(levelname)s - %(message)s')
        myconsole.setFormatter(formatter2)
        # add the handlers to the logger
        self.logger.addHandler(myfh)
        self.logger.addHandler(myconsole)
        self.logger.info('created an instance of: ' + filename)
        return self.logger 

def main():
    loggerinit = debuglogger()
    appname = ''
    filename = ''
    logger1 = loggerinit.loggerstart()
    
    logger1.debug('Quick zephyrs blow, vexing daft Jim.')
    logger1.info('How quickly daft jumping zebras vex.')
    logger1.warning('Jail zesty vixen who grabbed pay from quack.')
    logger1.error('The five boxing wizards jump quickly.')
    



        

'''
Function Calls
'''
if __name__ == '__main__':
    main()








