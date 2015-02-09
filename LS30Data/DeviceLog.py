'''
Created on Feb 9, 2015

@author: rpavlyuk
'''

from LS30Util import Commands


eventCommandPath = "commands.spec_commands.event"



def makeLogListEntry(number=0, code="", event="None", zone="", event_type="", activated=0, date="", time="", device_name=""):
    
    logEntry =  {"number": number, "code": code, "event": event, "zone": zone, "event_type": event_type, "activated": activated, "date": date, "time": time, "device_name": device_name}     
    return logEntry


def getTotalEventsCount():
    
    eventsCount = 0
    
    return 


def getDeviceLog(entryStart=0, entryEnd=25):
    
    global eventCommandPath
    
    logEntryList = [ makeLogListEntry(1), makeLogListEntry(2) ]
    
    Commands.loadCommandsFromFile()
    
    logCommandJSON = Commands.getCommandJSON(eventCommandPath)
    
    
    
    return logEntryList
    
    
    
    