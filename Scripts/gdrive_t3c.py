import os 
import logging
import sys
from shutil import copyfile

import tkinter as tk
from tkinter import filedialog


"""
creates directory without larges files from google drive folder and keep the google doc files since they do not take up space


"""

suffixlist = ['.gdoc', '.gslides','.gsheet', '.gmap']

appname = 'gdoc'
mylogger = logging.getLogger(appname)
mylogger.setLevel(logging.DEBUG)
myconsole = logging.StreamHandler()

myconsole.setLevel(logging.INFO)
formatter2 = logging.Formatter('%(levelname)s - %(message)s')
myconsole.setFormatter(formatter2)
mylogger.addHandler(myconsole)

def chkgdoc(rootdir):
    ifexist = False
    count = 0 
    for path, subdirs, files in os.walk(rootdir):
        for filename in files:
            filename_only, file_extension = os.path.splitext(filename)
            if file_extension in suffixlist:
                ifexist = True
                count = count + 1
                mylogger.info(path+'\\'+filename) 
    return ifexist, count

def loopandmirror(rootdir, outputroot):    #only folders with gdoc in it
    count = 0 
    for path, subdirs, files in os.walk(rootdir):
        for filename in files:
            infilepath = os.path.join(path, filename)
            mylogger.debug(os.path.join(path, filename) )
            pathdiff = os.path.relpath(path, rootdir)
            mylogger.debug(pathdiff)
            outfilepath = os.path.join(outputroot, pathdiff, filename)
            outfolderpath = os.path.join(outputroot, pathdiff)
            exists = os.path.isfile(outfilepath)
            if exists: 
                print("File already exits!  " + outfilepath)
            else:
                filename_only, file_extension = os.path.splitext(filename)
                if file_extension in suffixlist: #and if there is gdocs in this dir 
                    if not os.path.exists(outfolderpath):                     
                        mylogger.debug("directory %s is created." %outfolderpath)
                        os.makedirs(outfolderpath)
                        #the folder created should not contain filename

                    copyfile(infilepath, outfilepath)
                    count = count + 1
                    mylogger.info("File copied!  " + outfilepath)
                    
                elif checkext(file_extension):
                    mylogger.info("File suspicious!  " + outfilepath)
                else:
                    pass
                    #mylogger.info("File known not gdoc, skipped" + filename)
    print("File copied total =  " + str(count))

def checkext(extname):
    isSuspicious = False
    if extname == '':
        isSuspicious = True 
    elif extname.startswith('.g'):
        isSuspicious = True 
    else: 
        pass
    return isSuspicious


def main():
    root = tk.Tk()
    root.withdraw()
    mylogger.info('realpath {}'.format(os.path.realpath(__file__)) )
    pathandfolder = filedialog.askdirectory(initialdir = os.path.realpath(__file__))

    path, targetfoldername = os.path.split(pathandfolder)
    newfoldername = targetfoldername + '_gdoc'
    dir_path = path
    rootdir = os.path.join(dir_path, targetfoldername)
    outputroot = os.path.join(dir_path, newfoldername)
    mylogger.info(rootdir)
    mylogger.info(outputroot)
    toproceed, count = chkgdoc(rootdir)
    if toproceed:
        mylogger.info('Number of gdoc files in dir : ' + str(count) )
        if not input("Want to proceed? (y/n): ").lower().strip()[:1] == "y": sys.exit(1)
        loopandmirror(rootdir, outputroot)
        mylogger.info('Folder Mirrored')
    else: 
        mylogger.info('There is no gdoc in folder selected')

if __name__ == '__main__':
    main()
