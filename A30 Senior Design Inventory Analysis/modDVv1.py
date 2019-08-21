'''
Created on Oct 20, 2018

@author: Jean_Claude
'''

import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt

import modDSv1


class datavisualization(object):
    def __init__(self, statusdata):
        self.null = statusdata.getnull()
        self.notnull= statusdata.getnotnull()
        
        # Data to plot
        self.labels = 'Null', 'Not Null'
        self.values = [self.null, self.notnull]
        self.colors = ['yellowgreen', 'lightcoral']
        self.explode = (0.1, 0)  # explode 1st slice
    
    def make_autopct(self,values):
        def my_autopct(pct):
            total = sum(values)
            val = int(round(pct*total/100.0))
            return '{p:.2f}%  ({v:d})'.format(p=pct,v=val)
        
        return my_autopct
    
    def plot(self):
        # Plot
        plt.pie(self.values, explode=self.explode, labels=self.labels, colors=self.colors,
                shadow=True, startangle=140, autopct=self.make_autopct(self.values))
         
        plt.axis('equal')
        plt.suptitle('Result')
        plt.gcf().canvas.set_window_title('Null Search Bot')
        plt.show()
    
if __name__ == '__main__':
    mystatusdata = modDSv1.statusdata()
    mystatusdata.raw = [['DS28C22Q+U', False], ['asdfsadfaf', True], ["relay", False]]
    mystatusdata.mode = "APAC"
    
    print(mystatusdata.getnull())
    mydv = datavisualization(mystatusdata)
    mydv.plot()

    
    
