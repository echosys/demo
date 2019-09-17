
'''
This version last modified on 


''' 

import sqlite3
import iologgerv2 

import logging 

"""Do not name sqlite3, will confuse with library"""
class sqlite3db(object):   
    def __init__(self, dbname):
        self.dbname = dbname
        self.conn = ''
        self.logger1 = ''
    
    def connStart(self, logger1):
        #self.logger1 = logging.getLogger(loggername)
        self.logger1 = logger1 
        
        try:
            self.conn = sqlite3.connect(self.dbname)
            self.logger1.info("Opened database successfully");
        except Error as e:
            self.logger1.error(e)
    def connClose(self):
        self.conn.commit()   
        self.conn.close()    
        self.logger1.info("Closed database successfully");
        
    def createtabledata(self):
        self.conn.execute('''CREATE TABLE dir19Sum
                 (eid  INT PRIMARY KEY     NOT NULL,
                 name       TEXT    NOT NULL,
                 semester           TEXT    NOT NULL,
                 email          TEXT      NOT NULL,
                 desc1        TEXT,
                 desc2        TEXT,
                 imglink        TEXT,
                 weblink        TEXT,
                 isfaculty      TEXT,
                 updatetime        INT,
                 updatetimestr     TEXT,
                 inserttime        INT,
                 inserttimestr     TEXT,
                 
                 oldinfo1       TEXT,
                 oldinfo2       TEXT,
                 detail1        TEXT,
                 detail2        TEXT,
                 detail3        TEXT,
                 detail4        TEXT,
                 isstu          TEXT);''')
                 
        self.conn.execute('''CREATE TABLE dir19Log
                 (timestampms  INT PRIMARY KEY     NOT NULL,
                 timestampstr       TEXT,
                 changetype    TEXT    NOT NULL,
                 eid           TEXT    NOT NULL,
                 changeditems  TEXT,
                 olddict       TEXT,
                 newdict       TEXT);''')
        self.logger1.info("Tables created successfully");
    
    def create_row(self, personClass):
        """
        Create a new task
        :param conn:
        :param task:
        :return:
        """
     
        sqlinsert = ''' INSERT INTO dir19Sum(eid, name,semester,email,desc1,desc2,imglink,weblink, isfaculty, inserttime, inserttimestr)
                  VALUES(?,?,?,?,?,?,?,?,?,?,?) '''
        cur = self.conn.cursor()
        cur.execute(sqlinsert, personClass.toTuple() )
        self.logger1.info("New entry created successfully: " + str(cur.lastrowid) );
        self.conn.commit() 
        return cur.lastrowid
    
    def create_row_stufac(self, personClass, isstu):
        tablename = 'dir19Sum_stu' if isstu else 'dir19Sum_fac'
        sqlinsert = "INSERT INTO " + tablename + '''(eid, name,semester,email,desc1,desc2,imglink,weblink, isfaculty, inserttime, inserttimestr)
                  VALUES(?,?,?,?,?,?,?,?,?,?,?) '''
        cur = self.conn.cursor()
        cur.execute(sqlinsert, personClass.toTuple() )
        self.logger1.info("New entry created-"+ tablename + " " + str(cur.lastrowid) );
        self.conn.commit() 
        return cur.lastrowid
    
    
    def create_log(self, compare_res_str):
     
        sqlinsert = ''' INSERT INTO dir19Log(timestampms,timestampstr,changetype,eid,changeditems,olddict,newdict)
                  VALUES(?,?,?,?,?,?,?) '''
        cur = self.conn.cursor()
        cur.execute(sqlinsert, tuple(compare_res_str ) )
        self.logger1.info("Log created successfully: " + str(cur.lastrowid) );
        self.conn.commit() 
        return cur.lastrowid
    
    def update_row(self, personClass):
        # %s do not work in sqlite
        sqlupdate = ''' UPDATE dir19Sum SET name=?,semester=?,
        email=?,desc1=?,desc2=?,imglink=?,weblink=?,isfaculty=?, updatetime=?, updatetimestr=? WHERE eid=?
                  '''
        cur = self.conn.cursor()
        #first to last, pop first, append to last 
        newlist = personClass.toList()
        #newlist = newlist.append(newlist.pop(0) ) this is null
        newlist.append(newlist.pop(0) )
        #cursor.execute(sqlupdate, (var1,... var10, id))
        cur.execute(sqlupdate, tuple(newlist) )
        self.logger1.info("Entry updated successfully: " + str(cur.lastrowid) );
        self.conn.commit() 
        return cur.lastrowid
    
    def update_row_stufac(self, personClass, isstu):
        tablename = 'dir19Sum_stu' if isstu else 'dir19Sum_fac'
        sqlupdate = "UPDATE " + tablename + ''' SET name=?,semester=?,
        email=?,desc1=?,desc2=?,imglink=?,weblink=?,isfaculty=?, updatetime=?, updatetimestr=? WHERE eid=?'''
        
        cur = self.conn.cursor()
        newlist = personClass.toList()
        newlist.append(newlist.pop(0) )
        cur.execute(sqlupdate, tuple(newlist) )
        self.logger1.info("Entry updated-" + tablename + " " + str(cur.lastrowid) );
        self.conn.commit() 
        return cur.lastrowid
       
    def read_row(self, personClass):
     
        sqlselect = ''' SELECT eid,name,semester,email,desc1,desc2,imglink,weblink,isfaculty,inserttime FROM dir19Sum WHERE eid = ? 
                  '''
        cur = self.conn.cursor()
        cur.execute(sqlselect, (personClass.eid, ) )
        result = cur.fetchone()
        self.logger1.debug("Entry read successfully: " + str(list(result)) );
        return list(result)       
        
    def ifexist(self, personClass):
        ifexist = False
        sqlcheckexist  = "SELECT EXISTS(SELECT 1 FROM dir19Sum WHERE eid=? LIMIT 1);"
        cur = self.conn.cursor()
        cur.execute(sqlcheckexist, (personClass.eid,) )
        mydata = cur.fetchall() #[(0,)] not found, [(1,)] found 
        if mydata[0][0] == 0:
            ifexist = False
            self.logger1.info('There is no component named %s' % personClass.eid)
        else:
            ifexist = True
            self.logger1.info('Component %s found with eid, code %s'%(personClass.eid,','.join(map(str, next(zip(*mydata))))))
            #star is unpack https://stackoverflow.com/questions/44233099
        return ifexist
    
    
    

def main() :
    mydb = sqlite3db()
    mydb.connStart()
    #mydb.createtable()
    
    person1 = ('x@asu.edu','19Sum','xa xb','1','desc1  adfsdf/n adfdsa','desc2  adfsdf/n adfdsa','www.alink.com','' )
    person2 = ('x2@asu.edu','19Sum','xa2 xb2','2','desc1  adfsdf/n adfdsa','desc2  adfsdf/n adfdsa','www.alink.com','' )
    person3 = ('x@asu.edu','19Sum','xa xb','3','desc1  adfsdf/n adfdsa','desc2  adfsdf/n adfdsa','www.alink.com','' )
    mydb.create_task(person1)
    mydb.create_task(person2)
    #mydb.create_task(person3)
    mydb.connClose()


if __name__ == '__main__':
    main()
