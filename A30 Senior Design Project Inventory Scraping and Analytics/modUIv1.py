'''
Created on Oct 19, 2018

@author: Jean_Claude
'''


import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

from tkinter import ttk
from tkinter import Frame, BOTH, Text, Menu, END, Button, Label, PhotoImage, Entry

import threading
import datetime
import os 
import platform
import time
import subprocess

import modDSv1
import modPyChrome
import modDVv1
import modCSVv1


class AppUI(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()
        parent.title("Avnet - Null Search Bot")
        self.myEntry = Entry(parent)
        self.myEntry.pack()
        self.myEntry.delete(0, END)
        self.myEntry.insert(0, "2")

        self.label = Label(parent, text="Avnet - Null Search Bot")
        self.label.pack()

        #self.stop_button = Button(parent, text="Stop Search")
        #self.stop_button.pack()
        
        #self.status_button  = Button(parent, textvariable=status_text, command=update_btn_text)
        self.status_button = Button(parent, text="Status: 0/0")
        self.status_button.pack()         

        self.close_button = Button(parent, text="Close", command=parent.quit)
        self.close_button.pack()

        # initialize an empty list, one for the keyword and the other for the result
        self.keywordList = []
        self.resultList = []

    def initUI(self):
        self.parent.title("Avnet - Null Search Bot (Beta Build)")
        self.pack(fill=BOTH, expand=1)
        menubar = Menu(self.parent)
        
        self.parent.config(menu=menubar)

        fileMenu = Menu(menubar, tearoff=0)
        fileMenu.add_command(label="Open", command=self.onOpen)
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=fileMenu)

        logo = PhotoImage(file="avnet_logo.gif")
        label = Label(image=logo)
        label.image = logo  # keep a reference!
        label.pack()

        self.txt = Text(self)
        # self.txt.pack(fill=BOTH, expand=1)
        self.txt.pack()

        members = "CSE485 Capstone Project\n" \
               "Team Members:\n" \
               "Lingtao Ge\n" \
               "Tydin Jarman\n" \
               "Kobi Laker\n" \
               "William Driggs-Campbell\n" \
               "Chenguang Li\n" \
               "Yuxue Zhou\n" \
               "Paul Witulski\n" \
               "Arturo Corrales\n\n"
        self.txt.insert(END, members)

        helper1 = 'Please use File->Open to select Spreadsheet (.csv)\n      that contains the list of search keywords.\n\n'
        self.txt.insert(END, helper1)
        helper2 = 'Filename needs to contain AMERICAS, APAC, or EMEA'
        self.txt.insert(END, helper2)

    def onOpen(self):
        ftypes = [('Excel Spreadsheets', '*.csv'), ('All files', '*')]
        dlg = filedialog.Open(self, filetypes=ftypes)
        fl = dlg.show()

        # check to see if the filename was not empty (ie. user cancelled)
        if fl != '':
            myData = modDSv1.statusdata()
            waittime = self.myEntry.get() 
            myData.wait = int(waittime)
            print(waittime)
            self.threadx = threading.Thread(target=self.threadManager, args=(fl,myData))
            self.threadx.start()
            while (not myData.done):
                statusstring = str(myData.getDone() ) + '/' + str(len(myData.raw)-1 )
                #print(statusstring)
                self.status_button["text"] = statusstring
                #self.status_button.config(text=statusstring )
                time.sleep(3)
                
            myDV = modDVv1.datavisualization(myData)
            myDV.plot()  #the plot has to be in the same thread as Tkinter
    
    def startProcess1(self):
        pyfilepath = os.path.dirname(os.path.abspath(__file__))
        ostype = platform.system()
        chromefp = pyfilepath + "\chrome-win\chrome.exe"
        if (ostype == "Darwin"):
            chromefp = pyfilepath + "/chrome-mac/chromium.app/Contents/MacOS/Chromium"
        cmd = chromefp + " --remote-debugging-port=9222"
        print(pyfilepath)
        print(cmd)
        
        #os.system(cmd)  #this does not stop  
        subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        
        print('init done')
        
    def startProcess2(self, fnfull, myData):
        #init all classes 
        
        myCSV = modCSVv1.CSVhandler(myData)
        myCrawler = modPyChrome.PyChrome(myData)
        
        
        fnonly = os.path.splitext(fnfull)[0]
        print(fnonly)
        if "AMERICAS" in fnonly: 
            myData.mode = "AMERICAS"
        elif "APAC" in fnonly: 
            myData.mode = "APAC"
        elif "EMEA" in fnonly: 
            myData.mode = "EMEA"
        else:
            mydata.mode = "AMERICAS"
            print("error, filename needs to contain AMERICAS, APAC, or EMEA")
        
        myData.fnfull = fnfull
        myData.fnonly = fnonly  
        myCSV.readcsv()
        myCrawler.checknullall()
        
        myCSV.writecsv()   
        print("debug1: csv write done")
        
        #kill chromium process, release thread 
        ostype = platform.system()
        killcmd = "taskkill /f /im chrome.exe"
        if (ostype == "Darwin"):
            killcmd = "killall Chromium"
            
        #os.system(killcmd)   #careful, this closes all chrome instance    #use subprocess, system do not capture SIGNAL, thread do not stop
        subprocess.Popen(killcmd, stdout=subprocess.PIPE, shell=True)
        print("debug2: kill chromium done")
        time.sleep(3)         #some data processing needs chrome elements, kill before new run


    
    def threadManager(self, fl, myData):
        self.startProcess1()
        time.sleep(3) 
        self.startProcess2(fl, myData)
        print("debug3: thread manager done")


def main():
    root = tk.Tk()
    root.update()
    gui = AppUI(root)
    gui.mainloop()
    time.sleep(0.1)
    
    
    
    
main()


