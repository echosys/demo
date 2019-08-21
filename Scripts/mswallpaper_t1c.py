import os 
import logging
from shutil import copyfile

import tkinter as tk
from tkinter import filedialog

from PIL import Image



"""
This script extracts the MS spotlight photo on client computer
"""

userprofile = os.environ['USERPROFILE'] #C:\Users\USERNAME\
appdata = "AppData\Local\Packages\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\LocalState\Assets"
spotlightpath = os.path.join(userprofile, appdata)

outputpath = r'Pictures\python assets'
outputcache = r'Pictures\python raw'
outputpath =  os.path.join(userprofile, outputpath)
outputcache =  os.path.join(userprofile, outputcache)

appname = 'mswp'
mylogger = logging.getLogger(appname)
mylogger.setLevel(logging.DEBUG)
myconsole = logging.StreamHandler()
myconsole.setLevel(logging.DEBUG)
formatter2 = logging.Formatter('%(levelname)s - %(message)s')
myconsole.setFormatter(formatter2)
mylogger.addHandler(myconsole)

def copyandrename():
    ifexist = False
    count = 0 

    mylogger.debug(spotlightpath)
    for folderpath, subdirs, files in os.walk(spotlightpath):
        for eachfile in files:
            #mylogger.debug(eachfile, outputcache)
            outputcachefile = os.path.join(outputcache, eachfile)   
            infilepath = os.path.join(folderpath, eachfile)
            #mylogger.debug(filepath, outputcachefile)
            copyfile(infilepath, outputcachefile)     
                
    for folderpath, subdirs, files in os.walk(outputcache):
        for eachfile in files:
            filename_only, file_extension = os.path.splitext(eachfile)
            infilepath = os.path.join(folderpath, eachfile)        
            jpgsize = os.path.getsize(infilepath)
            im = Image.open(infilepath)
            width, height = im.size
            if checkdim(width, height):
                outpathfile = os.path.join(outputpath, eachfile) 
                copyfile(infilepath, outpathfile)
                renamepath = os.path.join(outputpath, filename_only + '.jpg') 
                try: 
                    os.rename(outpathfile, renamepath)
                except Exception as e: 
                    mylogger.error(e)
                    os.remove(outpathfile)
                #this still copies file if rename does not go through

def checkdim(w, h):
    iswallpaper = False
    #mylogger.debug(w, h)
    if w == 1920 and h == 1080: 
        iswallpaper = True
    elif w == 1080 and h == 1920: 
        iswallpaper = True
    return iswallpaper

def main():
    copyandrename()

    
if __name__ == '__main__':
    main()
