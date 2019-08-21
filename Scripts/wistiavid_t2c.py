import re
import json
import requests
import os 
import time 
import logging 
import math

from bs4 import BeautifulSoup
from tqdm import tqdm
    

'''
The wistia video link do not require login to access even thought the instructure page does.
This script demonstrate this exploit by parsing the webpage and extract direct download links embedded in the javascript
We have informed Wistia about this issue. 

progress bar, relative path work on any client computer


https://asu.instructure.com/courses/18145/pages/introduction-to-stable-matching?module_item_id=977918

startfromsrc url 
while has next checkifhaslink, next
extract lesson number and download
html2vid(htmlpage, quality, week, lesson)
    
'''

appname = 'wistiavid'
mylogger = logging.getLogger(appname)
mylogger.setLevel(logging.DEBUG)
myconsole = logging.StreamHandler()
myconsole.setLevel(logging.DEBUG)
formatter2 = logging.Formatter('%(levelname)s - %(message)s')
myconsole.setFormatter(formatter2)
mylogger.addHandler(myconsole)

ifprompt = True
dlfolder = 'wistiadl'

def main():  
    mystart = 'wk1_L1c.html'
    myfolder = 'wistiahtml'
    allfolderdl(startfile = mystart, stopfile=mystart, foldername = myfolder)
    
def allfolderdl(startfile='wk7_L1.html', stopfile='wk7_L1.html', quality='720p', foldername='551htmlsrc'):
    '''
    quality  #224p, 540p, 720p 1080p  Original file
    '''
    dir_path = os.path.dirname(os.path.realpath(__file__))
    folderloc = os.path.join(dir_path, foldername)
    #mylogger.debug(folderloc)
    allhtml = []
    for root, dirs, files in os.walk(folderloc):
        for file in files:
            if file.endswith('.html'):
                allhtml.append(file)               
    #mylogger.debug(allhtml)
    allhtml.sort()
    #mylogger.debug(allhtml)
    start = allhtml.index(startfile)
    stop = allhtml.index(stopfile)
    #ternary if same we still want 1 file
    list2dl = [] #list append returns nonetype
    list2dl = allhtml[start:stop+1] #if start == stop else allhtml[start:stop]
    #sublist do not index out of bound, but if start=step returns [], else stop not included in sublist
    mylogger.info(list2dl)
    if ifprompt: input("Press Enter to continue...")
    for filename in list2dl: 
        mylogger.info(filename)
        week=int(filename[2]) 
        lesson=int(filename[5])
        htmlpage = openhtmlfromfile(foldername, filename) 
        html2vid(htmlpage, quality, week, lesson)
        mylogger.info(week) 
        mylogger.info(lesson)

def downloadtqdm(url, filename): 
    '''
    https://stackoverflow.com/questions/37573483/
    '''
    
    r = requests.get(url, stream=True)
    # Total size in bytes.
    total_size = int(r.headers.get('content-length', 0)); 
    block_size = 1024
    wrote = 0 
    folderloc = os.path.join(os.path.dirname(os.path.abspath(__file__) ), dlfolder)
    if not os.path.exists(folderloc):
        os.makedirs(folderloc)
    fileloc = os.path.join(folderloc, filename)
    
    mylogger.info("dl location - {}".format(fileloc) )  
    with open(fileloc, 'wb') as f:
        for data in tqdm(r.iter_content(block_size), total=math.ceil(total_size//block_size) , unit='KB', unit_scale=True):
            wrote = wrote  + len(data)
            f.write(data)
    if total_size != 0 and wrote != total_size:
        mylogger.error("ERROR, something went wrong during dl")  

def openhtmlfromfile(myfolder, filename):
    foldername = ''.join(['.\\', myfolder])
    fileloc = os.path.join(foldername, filename)
    return open(fileloc)

def loopvid(allsrc, alltitle, ifdl, quality, week, lesson): 
    numtitle = len(alltitle)
    for i in range(numtitle ): 
        eachsrc = allsrc[i]
        eachtitle = alltitle[i]
        vidpage = requests.get(eachsrc)
        
        #find different quality
        vidcontent = BeautifulSoup(vidpage.content, "html.parser")
        pattern = re.compile(r'display_name')
        allscripts = vidcontent.findAll('script', text=pattern) 
        vidurljson = type(allscripts[0])
        vidurljson = allscripts[0].text.split('W.iframeInit(')[1].split(', {});')[0]
        #mylogger.debug(vidurljson)
        parsed = json.loads(vidurljson)
        #mylogger.debug(json.dumps(parsed, indent=4, sort_keys=True))
        #options  224  360*has three then 2 540 720 1080  "Original file"
        jsonvidlist = parsed['assets']
    
        vidcount = None    
        vidcount = 0
        for index, eachvidjson in enumerate(jsonvidlist):
            if eachvidjson['display_name'] == quality:
                vidcount = vidcount + 1
            mylogger.info(eachtitle +'-'+ quality +'-' + str(vidcount) + ' parts')
        
        for index, eachvidjson in enumerate(jsonvidlist):
            vidcount = 0
            if eachvidjson['display_name'] == quality:
                url = eachvidjson['url']
                #given the size in bytes, you need to divide by 1048576 (i.e. 1024 * 1024):
                response = requests.head(url).headers['Content-length']
                mb = int(response)/1048576 
                if(mb>0):
                    vidcount = vidcount + 1
                    mylogger.info('    ----part' + str(vidcount)+'-'+str(int(mb)) + 'MB')
                    thistitle = re.sub(r'[\W_]+', '', eachtitle)[5:] #remove title string iteral
                    thistitle = thistitle[:-5] #remove title string iteral
                    filename = 'U'+ str(week) +'L'+str(lesson)+'_' + str(i) + '_' + thistitle + '-' + str(vidcount) + '.mp4'
                    mylogger.info(filename)
                    if(ifdl): #if size>0   
                        #360p only first one, later ones missing frames
                        logstring = '    ------now getting---{} out of {} ----{}'.format(i+1,numtitle,url)
                        mylogger.info(logstring)
                        logstring = 'quality is {}-size = {} MB'.format(quality, int(mb))
                        mylogger.info(logstring)
                
                        downloaded = requests.get(url)
                        # week + vid + title + part1/2 
                        downloadtqdm(url, filename)
                        #break

def html2vid(htmlpage, quality, week, lesson):
    mylogger.info('week ' + str(week))
    soup = BeautifulSoup(htmlpage, "html.parser")
    allscripts = soup.find_all('script')
    for eachscript in allscripts:
        #mylogger.info(eachscript)
        pass
    
    #find the script with iframe link
    pattern = re.compile(r'INST = ')
    allscripts = soup.findAll('script', text=pattern) 
    splitonce = allscripts[0].text.split(';', 1)
    inst = splitonce[0]
    env = splitonce[1]
    env = env.replace("ENV = ", "")
    env = env[:-2]
    #mylogger.debug(env)  #iframe in env json
    parsed = json.loads(env)
    #mylogger.debug(json.dumps(parsed['WIKI_PAGE'], indent=4, sort_keys=True))
    jsonwp = parsed['WIKI_PAGE']['body']
    htmlwp = BeautifulSoup(jsonwp, "html.parser")

    '''
    target src=\"https://fast.wistia.net/embed/iframe/brm7mrx?videoFoam=true\"
    regex "src=\\\"https://fast.wistia.net/embed/iframe/.+?\?videoFoam=true\\\""
    urlpattern = "src=\\\"https://fast.wistia.net/embed/iframe/.+?\?videoFoam=true\\\""
    
    raw vid is huge, but one piece, dl then compress 
    720p is smaller, but in 2 piece, need to merge 
    '''
    urlpattern = "https://fast.wistia.net/embed/iframe/.+?\?videoFoam=true"
    resrc = re.compile(urlpattern)
    allsrc = re.findall(resrc, jsonwp)
    numlinkonpage = str(len(allsrc))
    mylogger.info('Number of Videos: There are ' + numlinkonpage)  
    mylogger.info("\n    ".join(allsrc))
    
    titlepattern = "title=\\\".+?\\\""
    retitle = re.compile(titlepattern)
    alltitle = re.findall(retitle, jsonwp)
    numtitleonpage = str(len(alltitle))
    mylogger.info('Number of Videos: There are ' + numtitleonpage) 
    mylogger.info("\n    ".join(alltitle))   
    
    if numlinkonpage == numtitleonpage: 
        mylogger.info('number of title match link')
    else:
        mylogger.error('ERROR number of title do not match link')
        alltitle = alltitle[:len(allsrc)]
        mylogger.error(alltitle)
    #get vid size and number for each title
    loopvid(allsrc, alltitle, False, quality, week, lesson)
    #download each part in each page
    if ifprompt: input("Press Enter to continue...")
    time.sleep(5)
    loopvid(allsrc, alltitle, True, quality, week, lesson)
 
if __name__ == '__main__':
    main()


