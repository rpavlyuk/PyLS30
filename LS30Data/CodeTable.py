'''
Created on Feb 22, 2015

@author: rpavlyuk
'''


from LS30Util import Config
import json


def getEventNameByCode(eventCode):
    
    eventCodesFile = open(Config.getCodeTableEvents())
    
    eventsJSON = json.load(eventCodesFile)
    
    return eventsJSON[str(eventCode)]

