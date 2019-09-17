
'''
This version last modified on Nov 6, 2018

use sqlite3 

data analysis, export to one table 
        date
CSEXXX    openseats

logic 
if date = date and seats1>seats2 update
if not, add new column 

'''

import sqlite3
import sys

"""Do not name sqlite3, will confuse with library"""
class sqlite3db(object):   
    def __init__(self):
        self.raw = []
        self.conn = sqlite3.connect('test.db')
        print("Opened database successfully");
        
    def createtable1(self):
        self.conn.execute('''CREATE TABLE IF NOT EXISTS DATALOG
                 (TIMEINT INT PRIMARY KEY     NOT NULL,
                 CREGNUM        INT     NOT NULL,
                 CNUM           INT     NOT NULL,
                 CTITLE    CHAR(50),
                 DATESTR    TEXT,
                 TIMESTR TEXT,
                 STOTAL    INT,
                 SOPENMAX    INT,
                 SOPENTOTAL    INT,
                 SRESERV    INT,
                 OTHERINFO TEXT);''')
                                
                 #ADDRESS        CHAR(50),
                 #SALARY         REAL);''')
        print("Table created successfully");
    
    def insertt1(self):
        sql ="""
        INSERT INTO DATALOG (
        TIMEINT, CREGNUM, CNUM, CTITLE, DATESTR, TIMESTR, STOTAL, SOPENMAX, SOPENTOTAL, SRESERV, OTHERINFO)
        VALUES
        (1546495542, 32013, 573, "Semantic Web Mining", "Jan 1 2019", "11:07:35", 124, 0, 0,0,"[hr, loc, instructor]");"""
        #(1546495684, 33333, 599, "Min test data");"""
        cur = self.conn.cursor()
        self.conn.execute(sql)
        print("Table data inserted successfully");
        
        sql ="""
        INSERT INTO DATALOG (
        TIMEINT, CREGNUM, CNUM, CTITLE)
        VALUES
        (1546495684, 33333, 599, "Min test data");"""
        cur = self.conn.cursor()
        self.conn.execute(sql)
        print("Table data inserted successfully 2");
    
    def selectwheret1(self):    
        cur = self.conn.cursor()
        priority = 500
        cur.execute("SELECT * FROM DATALOG WHERE CNUM>=?", (priority,))
        rows = cur.fetchall()
        for row in rows:
            print(row)
    
    def committ1(self):
        self.conn.commit()
        print("Table data committed successfully");
    
    def dropt1(self):
        sql = 'DROP TABLE DATALOG'
        cur = self.conn.cursor()
        cur.execute(sql)
        print("Table dropped successfully");
        
    def selectt1(self):
        sql = """
        SELECT
         TIMEINT,
         CNUM
        FROM
         DATALOG
        ORDER BY
         TIMEINT DESC
        LIMIT 3;
        """
        cur = self.conn.cursor()
        cur.execute(sql)
        print("Table selected successfully");
        rows = cur.fetchall()
 
        for row in rows:
            print(row)
        
    def closeconn(self):
        self.conn.close()

def main() :
    mydb = sqlite3db()
    try:
        mydb.createtable1()
        #mydb.insertt1()
        mydb.selectt1()
        mydb.selectwheret1()
        #mydb.dropt1()
        mydb.committ1()
        mydb.closeconn()
    except:
        print("Unexpected error:", sys.exc_info()[0])
        print("-----Detail:", sys.exc_info()[1])
        raise


"""
comment out after test 
"""
main()
