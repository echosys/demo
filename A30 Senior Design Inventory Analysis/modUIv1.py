'''
Created on Oct 19, 2018

@author: Jean_Claude
'''


import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk

from tkinter import HORIZONTAL
from tkinter.ttk import Progressbar
from tkinter import Frame, BOTH, Text, Menu, END, Button, Label, PhotoImage, Entry

import threading
import subprocess
import datetime
import os 
import platform
import time
import sys

import modPyChrome
import modDSv1
import modDVv1
import modFilev1
import iologgerv2
from iologgerv2 import debuglogger

class AppUI(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)
        self.parent = root

    def initUI(self, root):
        self.parent.title("Avnet Inventory Compare Beta")
        self.pack(fill=BOTH, expand=1)
        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)

        fileMenu = Menu(menubar, tearoff=0)
        fileMenu.add_command(label="Open", command = self.onOpen)
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", command = self.closeUI )
        menubar.add_cascade(label="File", menu = fileMenu)

        logo = PhotoImage(file="avnet_logo.gif")
        label = Label(image=logo)
        label.image = logo
        label.pack()

        self.body = Text(self)
        self.body.pack() # self.txt.pack(fill=BOTH, expand=1)
        body1 = "CSE Capstone Project\n" + "Lingtao Ge\n"
        body2 = 'Please use File->Open to select Spreadsheet (.csv)\n      that contains the list of keywords.\n\n'
        body3 = 'Subdomain selection uses AMERICAS, APAC, or EMEA in Filename'
        self.body.insert(END, body1)
        self.body.insert(END, body2)
        self.body.insert(END, body3)
        
        #custom crawling speed
        self.myEntry = Entry(self.parent)
        self.myEntry.pack()
        self.myEntry.delete(0, END)
        self.myEntry.insert(0, "1")
        self.label = Label(self.parent, text="Waittime in sec(s)")
        self.label.pack()

        #stop replaced by close
        self.status_button = Button(self.parent, text="Status: 0/0")
        self.status_button.pack()         
        self.pbar = Progressbar(self.parent,orient=HORIZONTAL,length=100,mode='determinate')
        self.pbar.pack()
        self.close_button = Button(self.parent, text="Close", command = self.closeUI )
        self.close_button.pack()
        
        #logger start 
        loggerinit = debuglogger()
        appname = "InventoryBot"
        filename = 'debug_%s.txt' %appname
        logger1 = loggerinit.loggerstart(appname, filename)
        self.logger = logger1
        self.myData = ''

    def closeUI(self):
        self.parent.destroy()
        #self.parent.quit()  #only works before threads start
    
    def onOpen(self):
        ftypes = [('Excel Spreadsheets', '*.csv'), ('All files', '*')]
        askpath_title = 'Please select csv containing keywords'
        askpath_default = os.path.dirname(os.path.abspath(__file__))
        filename = filedialog.askopenfilename(initialdir = askpath_default,title = askpath_title,filetypes = ftypes)
        
        print(filename)
        # check to see if the filename was not empty (ie. user cancelled)
        try:
            if filename:
                myData = modDSv1.statusdata()
                myData.logger = self.logger
                self.myData = myData
                
                self.threadx = threading.Thread(target=self.threadManager, args = (filename,myData))
                self.threadx.start()
                waittime = self.myEntry.get() 
                myData.wait = int(waittime)
                self.logger.info('Now starting with waittime {}'.format(waittime) )

                self.parent.after(1000, self.plotResults)
            else: 
                self.logger.error("User did not select a file")
        except:
            self.logger.error("Unexpected error:", sys.exc_info()[0])
            self.logger.error("-----Detail:", sys.exc_info()[1])
            raise
            sys.exit("User did not select a file")
        
    def plotResults(self):     
        if(self.myData.done):
            myDV = modDVv1.datavisualization(myData)
            #the plot has to be in the same thread as Tkinter, shared Canvas
            myDV.plot()  
        else:
            numdone = self.myData.getStatus_fromdict()['numdone']
            numtotal = self.myData.getStatus_fromdict()['numtotal']
            statusstring = '{}/{}'.format(numdone, numtotal)
            self.status_button["text"] = statusstring
            self.pbar['value'] = 0 if numdone or numtotal == 0 else int(numdone/numtotal*100)
            self.parent.after(1000, self.plotResults)
            
    def threadManager(self, filepath, myData):
        self.startChromium1()
        time.sleep(3) #wait for chrome to launch
        self.startDataLogging2(filepath, myData)
        self.logger.info("debug3: thread manager done")
        
    def startChromium1(self):
        istest = True
        pyfilepath = os.path.dirname(os.path.abspath(__file__))
        ostype = platform.system()
        if ostype == 'Windows': 
            chromefp = os.path.join(pyfilepath, 'chrome-win', 'chrome.exe') if istest else os.path.join(pyfilepath, 'chrome-win', 'chrome.exe') #deploy
        elif ostype == 'Darwin': 
            chromefp = os.path.join(pyfilepath, 'chrome-mac', 'chromium.app', 'Contents', 'MacOS', 'Chromium')
        elif ostype == 'Linux': 
            self.logger.info('to be implemented')
        cmd = ' '.join([chromefp, "--remote-debugging-port=9222"])
        
        #how to start and get process ID 
        #os.system(cmd)  #can not stop programmatically  
        myprocess = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=False)
        #the pid of the shell if shell True or pid of the chrome it opens shell False
        self.processid = myprocess.pid 
        self.logger.info('ostype is {}, start cmd is {}'.format(ostype, cmd) )
        self.logger.info('pid is {}'.format(self.processid) )
        
    def startDataLogging2(self, filepath, myData):
        myInput = modFilev1.Filehandler(myData)
        myCrawler = modPyChrome.PyChrome(myData)
    
        fnonly = os.path.split(filepath)[1]
        self.logger.info(fnonly)
        if "AMERICAS" in fnonly: 
            myData.mode = "AMERICAS"
        elif "APAC" in fnonly: 
            myData.mode = "APAC"
        elif "EMEA" in fnonly: 
            myData.mode = "EMEA"
        else:
            mydata.mode = "AMERICAS"
            self.logger.info("Default US, Subdomain uses AMERICAS, APAC, or EMEA in Filename")
        
        myData.filepath = filepath
        myData.fnonly = fnonly  
        
        myInput.readCsv_asdict()
        #myCrawler.checknullall() #for stop cont function
        myCrawler.runandRecord()
        
        #myCSV.writecsv()   
        self.logger.info("debug1: csv write done")
        
        #kill chromium process, release thread 
        ostype = platform.system()
        if ostype == 'Windows': 
            #killcmd = "taskkill /f /im chrome.exe"
            killcmd = 'taskkill /F /PID {}'.format(mygui.processid)
        elif ostype == 'Darwin': 
            killcmd = "killall Chromium"
        elif ostype == 'Linux': 
            killcmd = "killall Chromium"
        self.logger.info("Save your progress, chrome will be closed until next run")
        time.sleep(5)
        #os.system(killcmd)   #careful, this closes all chrome instance    
        #use subprocess, system do not capture SIGNAL, thread do not stop
        subprocess.Popen(killcmd, stdout=subprocess.PIPE, shell=True)
        self.logger.info("debug2: kill chromium done")
        time.sleep(3)         #some data processing needs chrome elements, kill before new run





def main():
    root = tk.Tk()
    root.update()
    mygui = AppUI(root)
    mygui.initUI(root)
    mygui.mainloop()
    time.sleep(1)
    #code reach here are root.destory, close all chrome processes 
    killcmd = 'taskkill /F /PID {}'.format(mygui.processid)
    subprocess.Popen(killcmd, stdout=subprocess.PIPE, shell=True)
    
if __name__ == '__main__':
    main()


