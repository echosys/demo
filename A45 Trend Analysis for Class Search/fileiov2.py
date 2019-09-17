
'''
This version last modified on Nov 6, 2018


'''

#imports
import datetime
from time import gmtime, strftime, localtime
import sys
import logging


# import wcs_v2     # have to comment out when not testing this file # circular import at bottom or in function
from dsv1 import cse
import smtp_gmv1

class printstruct(object):
    def __init__(self):
        self.classnum = ''
        self.changedfield = ''
        self.filler1 = ' has changed from '
        self.curval = ''
        self.pastval = ''
        self.filler2 = ' to '
        self.level = 1
        self.curRawobject = None
        self.ischanged = False
        
    def toString(self):
        msg = self.classnum + ',' +  self.changedfield + ',' + self.filler1 + ','  + self.pastval + ',' \
        + self.filler2  + ',' + self.curval + '\n' + '      ' + '-----now ' + self.curRawobject.toString() 
        print(msg)    
        return msg    
'''
standard IO helper function
'''
def gettime():
    timestampUTC = datetime.datetime.now()
    timestrUTC = strftime("%Y-%m-%d %H:%M:%S", localtime())
    TD = datetime.timedelta(hours=7)  
    timestampAZ =  timestampUTC - TD 
    timestrAZ = timestampAZ.strftime("%Y-%m-%d %H:%M:%S")
    utcstr =  timestrUTC + '- time: UTC; '+ timestrAZ + '- time: AZ '
    #self.utcstr = strftime("%Y-%m-%d %H:%M:%S", localtime())   
    return utcstr    

            

def list2txt(array, filename): 
    with open(filename, "r+") as f:
        for row in array:
            f.write(row + "\n")
    
    f.close()

def txt2list(array, filename): 
    with open(filename, "r+") as f:
        array  = f.readlines()
        array  = [x.strip() for x in array ]
    
    f.close()
    return array 
        
def logtxt(array,filename):  
    try: 
        with open(filename, "r+") as f:
            content = f.read()
            f.seek(0, 0)
            #write to the top of the file 
            f.write("====================================================" + "\n") 
            f.write(gettime() + "\n") 
            for row in array:
                f.write(row + "\n")
            #write the file that was already there
            #f.write(self.utcstr + "\n")     
            f.write('\n' + content)
            #time.sleep(1)
        f.close()
    
    except:
        errorcode = ("2 Unexpected error in wr2txt:", sys.exc_info()[0])
        print(errorcode)
        raise  #re-raise the exception (allowing a caller to handle the exception as well)
    #end of wr2txt



'''
error log
    can handle multithread, can handle multiple file/module write

'''
class debuglogger(object):
    def __init__(self):
        self.logger = None
    
    def debugloggerstart(self,appname='server_log', filename='server.log'):
        # create logger with 'server_log'
        self.logger = logging.getLogger(appname)
        self.logger.setLevel(logging.DEBUG)
        # create file handler which logs even debug messages
        fh = logging.FileHandler(filename)
        fh.setLevel(logging.DEBUG)
        # create console handler with a higher log level
        #ch = logging.StreamHandler()
        #ch.setLevel(logging.ERROR)
        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        #ch.setFormatter(formatter)
        # add the handlers to the logger
        self.logger.addHandler(fh)
        #logger.addHandler(ch)
        self.logger.info('created an instance of: ' + filename)

    def dladd(self,msg):
        self.logger.info(msg)

'''
custom file compares


'''
def list2obj(printlist):
    objlist = []
    #print('debug2')
    #print(printlist)
    for eachrow in printlist:
        if (len(eachrow) > 1):   #the last line of file can be a blank or carriage return
            atts = eachrow.split(',')
            #print(eachrow,atts)
            cseclass = cse()
            cseclass.cnum = atts[0]
            cseclass.ctitle = atts[1]
            cseclass.cregnum = atts[2]
            cseclass.cseatsopen = atts[3]
            cseclass.cseatstotal = atts[4]
            cseclass.cindicator = atts[5] 
            objlist.append(cseclass)
    return objlist       
    
def datacompare(objlistcur, objlistlast):
    error = ''
    msg = ''
    printlist = []
    haschange = False
    for cur, past in zip(objlistcur, objlistlast):
        if cur.cnum == past.cnum: 
            if cur.cindicator != past.cindicator: #reserve/unavail to avail
                changedclass = printstruct()
                changedclass.classnum = cur.cnum
                changedclass.changedfield = 'STATUS'
                changedclass.curval = cur.cindicator
                changedclass.pastval = past.cindicator
                changedclass.level = 1
                changedclass.curRawobject = cur
                haschange = True
                printlist.append(changedclass)  
                
            if cur.cseatstotal != past.cseatstotal: #seats total increase
                changedclass = printstruct()
                changedclass.classnum = cur.cnum
                changedclass.changedfield = 'SEATTOTAL'
                changedclass.curval = cur.cseatstotal
                changedclass.pastval = past.cseatstotal
                changedclass.level = 1
                changedclass.curRawobject = cur
                haschange = True
                printlist.append(changedclass)
            
            if cur.cindicator == "seats available":    #avilable class has more seats
                if cur.cseatsopen > past.cseatsopen:
                    changedclass = printstruct()
                    changedclass.classnum = cur.cnum
                    changedclass.changedfield = 'SEATOPEN'
                    changedclass.curval = cur.cseatsopen
                    changedclass.pastval = past.cseatsopen
                    changedclass.level = 2
                    changedclass.curRawobject = cur
                    haschange = True
                    printlist.append(changedclass)
                 
            
        elif cur.cnum != past.cnum:
            #sth mess up the order or new class was added  
            error = 'Course ' + str(cur.cnum) + ' is now ' + str(past.cnum)
            print(error)
    return printlist

def sendonce(recipients, msg):
        mygmail = smtp_gmv1.smtpgmail()
        subject = '[BLT] Test Message From Class Finder Server'  
        bodytext = msg
        unsubinfo = '\n TO UNSUB filter by [BLT]'
        
        mygmail.setgmail(recipients)
        #mygmail.setoutlook(recipients)
        
        mygmail.sendemail(subject, bodytext, unsubinfo)
    
#test functions 
def main():
    #test 
    datapast = []
    datacur = []
    datapast = txt2list(datapast, "datapast.txt")
    datacur = txt2list(datacur, "datacur.txt")
    print(datapast)
    print(datacur)

    objcur = list2obj(datacur)
    objlast =  list2obj(datapast)
    print(objlast[0].cnum)
    printlist = datacompare(objcur, objlast) #datacompare cur last
    print(printlist)
    if len(printlist) > 0:
        msg = ''
        for eachprintstruct in printlist:
            msg = msg + "\n" + eachprintstruct.toString()
        sendonce(['gelingtao@gmail.com'], msg)



        

'''
Function Calls
'''
#main()








