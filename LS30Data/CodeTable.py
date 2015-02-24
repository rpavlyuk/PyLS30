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


def getEventTypeByCode(eventTypeCode):
    
    eventTypesFile = open(Config.getCodeTableEventTypes())
    
    eventTypesJSON = json.load(eventTypesFile)
    
    return eventTypesJSON[str(eventTypeCode)]

def getSensorGroupConfig():
    
    groupConfigFile = open(Config.getSensorGroupConfig())
    
    return json.load(groupConfigFile)