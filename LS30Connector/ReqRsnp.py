'''
Created on Feb 6, 2015

@author: rpavlyuk
'''
from serial import Serial

class ReqRsnp(object):
    '''
    classdocs
    '''

    connString  = "socket://home.pavlyuk.lviv.ua:1681"

    def __init__(self, params):
        '''
        Constructor
        '''
        

    def sendRequest(self):
        
        conn = Serial()
        
        conn.setPort(self.connString)
        
        conn.open()
        
        return 0;