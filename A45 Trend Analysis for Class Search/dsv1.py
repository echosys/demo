
'''
This version last modified on Nov 6, 2018

common data structure so that we can avoid circular import 
http://tinyurl.com/ycunbg9m
'''

class cse(object):
    def __init__(self):
        self.raw = []
        self.cnum = ''
        self.ctitle = ''
        self.cregnum = ''
        self.cdetail = ''
        self.cseatsopen = ''
        self.cseatstotal = ''
        self.cindicator = ''
    def toString(self):
        seperator = ', '
        mylist = [self.cnum, self.ctitle, self.cregnum, self.cseatsopen, 'of', self.cseatstotal, self.cindicator]
        msg = seperator.join(mylist)
        return msg



