
'''
This version last modified on

'''
import json
import ast 

class dirPerson(object):
    def __init__(self, logger1):
        self.raw = []
        self.email = ''
        self.name = ''
        self.semester = ''
        self.eid = ''
        self.desc1 = ''
        self.desc2 = ''
        self.imglink = ''
        self.weblink = ''
        self.detail1 = ''
        self.detail2 = ''
        self.detail3 = ''
        self.detail4 = ''
        
        self.updateTime = ''
        self.updateTimestr = ''
        self.insertTime = ''
        self.insertTimestr = ''
        self.oldInfo1 = ''
        self.oldInfo2 = ''
        self.isfaculty = ''
        self.isstu = ''
        
        self.logger = logger1 
            
    def toString(self):
        seperator = ', '
        mylist = [self.eid, self.name, self.semester, self.email, self.desc1, self.desc2, self.isfaculty]
        msg = ','.join(map(str, mylist))
        return msg
    
    def toTuple(self):
        seperator = ', '
        mylist = (self.eid, self.name, str(self.semester), self.email, self.desc1, self.desc2,
                  self.imglink, self.weblink, str(self.isfaculty), self.insertTime, self.insertTimestr)
        return mylist
    
    def toList(self):   
        #this makes it a list of strings, not list of objs
        seperator = ', '
        mylist = [self.eid, self.name, str(self.semester), self.email, self.desc1, self.desc2,
                  self.imglink, self.weblink, str(self.isfaculty), self.updateTime, self.updateTimestr]
        return mylist
    
    def compare(self, oldP, utctimems, utctimestr):
        ifupdate = False 
        changetype = 'sm'         # sm lg new

        dictOld = obj2dict(oldP)
        dictNew = obj2dict(self)
        # ^ vs - https://stackoverflow.com/questions/32815640
        #print(dictOld.items())
        setOld = set(dictOld.items())
        setNew = set(dictNew.items())
        #TypeError: unhashable type: 'list'
        setDiff = setOld - setNew
        dictDiff = dict(setDiff)
        #keys is view
        changedkeys = list(dictDiff.keys()) 
        lgchange = ['name','email','isfaculty']
        listDiff = changedkeys
        
        #contain test  isfaculty, semester 
        if 'isfaculty' in listDiff:
            result = all(elem in oldP.isfaculty for elem in self.isfaculty)
            if result:
                listDiff.pop(listDiff.index('isfaculty'))        
        if 'semester' in listDiff:
            result = all(elem in oldP.semester for elem in self.semester)
            if result:
                listDiff.pop(listDiff.index('semester'))     
        #ignore insertTime 
        if 'insertTime' in listDiff:
            listDiff.pop(listDiff.index('insertTime'))   
        #str vs int eid  
        if 'eid' in listDiff:
            listDiff.pop(listDiff.index('eid'))  
            
        if len(listDiff) == 0:
            ifupdate = False 
            
        else: 
            self.logger.info('%s %s' %(listDiff, oldP.eid) )
            ifupdate = True
            if bool(set(lgchange) & set(listDiff)):
                changetype = 'lg'
            else: 
                changetype = 'sm'
            
            oldP.name = self.name 
            oldP.email = self.email 
            oldP.desc1 = self.desc1 
            oldP.desc2 = self.desc2 
            oldP.imglink = self.imglink 
            oldP.weblink = self.weblink 
            oldP.updateTime = self.updateTime
            oldP.updateTimestr = self.updateTimestr
            
            oldP.semester = oldP.semester + list(set(self.semester) - set(oldP.semester))
            oldP.isfaculty = oldP.isfaculty + list(set(self.isfaculty) - set(oldP.isfaculty))
            #semester as a list, add each time it is still around [19Sum, 19Fall]
            #isfaculty as a list, add each aspect [faculty, stu]
        changeditems = str(listDiff)
        
        # convert to string
        dictOld_str = json.dumps(dictOld)
        dictNew_str = json.dumps(dictNew)
        #my_dict = json.loads(input) 
        newmyP = oldP
        return [ifupdate, newmyP, utctimems, utctimestr, changetype, oldP.eid, changeditems, dictOld_str, dictNew_str]

    
def list2obj(oldlist, logger1):
    #replace all none with '' becuase set(None) TypeError: 'NoneType' object is not iterable
    #set('') = None, we need sets for dict to be hashable, dict can not have lists 
    oldlist = ['' if x == None else x for x in oldlist]
    
    newP = dirPerson(logger1)
    newP.eid = oldlist[0]
    newP.name = oldlist[1]
    newP.semester = ast.literal_eval(oldlist[2] )
    newP.email = oldlist[3]
    newP.desc1 = oldlist[4]
    newP.desc2 = oldlist[5]
    newP.imglink = oldlist[6]
    newP.weblink = oldlist[7]
    newP.isfaculty = [] if len(oldlist[8]) == 0 else ast.literal_eval(oldlist[8] )
    newP.insertTime = oldlist[9]
    
    return newP 
    
def obj2dict(newP):
    pDict = {}
    pDict.update(eid = newP.eid)
    pDict.update(name = newP.name)
    pDict.update(semester = str(newP.semester) )
    #{'9', 'r', 'p', '1', 'S'} is from '19Spr'
    pDict.update(email = newP.email)
    pDict.update(desc1 = newP.desc1)
    pDict.update(desc2 = newP.desc2)
    pDict.update(imglink = newP.imglink)
    pDict.update(weblink = newP.weblink)
    #strisfaculty = str(newP.isfaculty) if newP.isfaculty
    pDict.update(isfaculty = str(newP.isfaculty) )
    pDict.update(insertTime = newP.insertTime)
    return pDict  



    
if __name__ == '__main__':
    main()    


