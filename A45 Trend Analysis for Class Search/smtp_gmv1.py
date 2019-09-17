

'''
This version last modified on Nov 6, 2018


'''

#imports
import sys

import datetime
from time import gmtime, strftime, localtime

import smtplib
from email.mime.text import MIMEText
from email.header    import Header

class  smtpgmail(object):
    
    def __init__(self):
        #gmail constants
        self.magnum = ''
        self.gmail_user = ''
        self.gmail_mima = ''
        self.sent_from = self.gmail_user
        self.sent_to = ''  
        self.recipients_emails = ['default@live.cn']  
        self.emailbody = ''
        self.emailstatus = ''
        self.emaillog = []
        self.emailbodytext = ''
        
        #content 
        self.subject = ''
        
    def gettime(self):
        timestampUTC = datetime.datetime.now()
        timestrUTC = strftime("%Y-%m-%d %H:%M:%S", localtime())
        TD = datetime.timedelta(hours=7)  
        timestampAZ =  timestampUTC - TD 
        timestrAZ = timestampAZ.strftime("%Y-%m-%d %H:%M:%S")
        self.utcstr =  timestrUTC + '- time: UTC; '+ timestrAZ + '- time: AZ '
        #self.utcstr = strftime("%Y-%m-%d %H:%M:%S", localtime())   
        
        
    def setgmail(self,recipients):
        #gmail setup
        # the plus sign means "and write also"
        with open("smtpxinxi.txt", "r+") as fo:
            line1 = fo.readline().strip()
            line2 = fo.readline().strip()
        print(line1)
        print(line2)
        fo.close()
        self.magnum = int(line2)
        self.gmail_user = line1 + '@gmail.com'  
        self.gmail_mima = '64' + str(0000 + (-34) + self.magnum) + str(1953)
        self.sent_from = self.gmail_user  
        #print(self.sent_from)
        #print(self.gmail_mima)
        
        self.recipients_emails = recipients
    
    def setoutlook(self,recipients):
        self.gmail_user = 'gelingtao@live.cn'
        self.gmail_mima = 'qwer6436'
        self.sent_from = self.gmail_user 
        self.recipients_emails = recipients
        
        
    def sendemail(self,subject, bodytext, unsubinfo):

        self.emailbody = bodytext + unsubinfo
        msg = MIMEText(self.emailbody, 'plain', 'utf-8')
        msg['Subject'] = Header(subject, 'utf-8')
        msg['From'] = self.sent_from
        msg['To'] = ", ".join(self.recipients_emails)
        self.emailstatus = 'debug:start sending emails'
        try:  
            print('Status: Email sending initiated...')
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)    
            #server = smtplib.SMTP('smtp-mail.outlook.com', 587) #outlook mailServer
            
            print('Attempting...')
            server.ehlo()
            
            #uncomment for outlook only
            #server.starttls()
            
            server.login(self.gmail_user, self.gmail_mima)
            print('Login...')
            server.sendmail(msg['From'], self.recipients_emails, msg.as_string())
            server.close()
            print('Email sent!')
            self.emailstatus = 'email sent...'
            entry = []
            entry.append(", ".join(self.recipients_emails))
            self.gettime()
            entry.append(self.utcstr)
            self.emaillog.append(entry)
            
        except:  
            self.emailstatus = 'email not sent...'
            print('Something went wrong...')
            print("Unexpected error:", sys.exc_info()[0])
            print("Unexpected error:", sys.exc_info()[1])
            raise

    def sendonce(self,recipients, msg):
            subject = '[BLT] Test Message From Class Finder Server'  
            bodytext = msg
            unsubinfo = '\n TO UNSUB filter by [BLT]'
            
            self.setgmail(recipients)
            #mygmail.setoutlook(recipients)
            
            self.sendemail(subject, bodytext, unsubinfo)            
    
def restart_line():
    sys.stdout.write('\r')
    sys.stdout.flush()
 
def main():
    #this is example of how to envoke smtp gmail class 
    mygmail = smtpgmail()
    
    msg = 'TypeError: sequence item 0: expected str instance, list found'
    #""" Test for send once functions
    mygmail.sendonce(['gelingtao@gmail.com'], msg)
    mygmail.sendonce(['gelingtao@live.cn'], msg)
    
    #"""
    
    
    """ Test for raw functions
    recipients = ['gelingtao@gmail.com']           
    subject = '[BLT] Test Message From Class Finder Server'  
    bodytext = 'This is a test'
    unsubinfo = '\n TO UNSUB filter by [BLT]'
    
    mygmail.setgmail(recipients)
    #mygmail.setoutlook(recipients)
    
    mygmail.sendemail(subject, bodytext, unsubinfo)
    """

'''
Function Calls
'''
#main()            #comment out when done testing, importing will can the main 







