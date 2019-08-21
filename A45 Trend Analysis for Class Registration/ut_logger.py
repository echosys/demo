
'''
This version last modified on Nov 6, 2018

'''
import fileiov2 

def main():
    logger = fileiov2.debuglogger()
    msg = fileiov2.gettime() + '\n' + 'test message' 
    logger.debugloggerstart()
    logger.dladd(msg)
    """ different options
    logger.debug('debug message')
    logger.info('info message')
    logger.warn('warn message')
    logger.error('error message')
    logger.critical('critical message')
    """
        
    
    
    
    
    









main()



