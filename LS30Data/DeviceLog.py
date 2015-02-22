'''
Created on Feb 9, 2015

@author: rpavlyuk
'''

from LS30Util import Commands
from LS30Connector import ReqRsnp
from LS30Data import CodeTable


eventCommandPath = "commands.spec_commands.event"



def makeLogListEntry(number=0, code="", event="None", zone="", event_type="", activated=0, date="", time="", device_name=""):
    
    logEntry =  {"number": number, "code": code, "event": event, "zone": zone, "event_type": event_type, "activated": activated, "date": date, "time": time, "device_name": device_name}     
    return logEntry


def getTotalEventsCount():
    
    eventsCount = 0
    
    return 


def getDeviceLog(connection, entryStart=0, entryEnd=25):
    
    global eventCommandPath
    
    recvString = ""
    count = 0
    
    logEntryListStr = [ ]
    
    logEntryList = [  ]
    
    Commands.loadCommandsFromFile()
    
    logCommandJSON = Commands.getCommandJSON(eventCommandPath)
    
    recvString = connection.sendCommand("ev000")
    memAddrStr = recvString[len(recvString)-3:]
    memAddr = int(memAddrStr, 16)
    
    print "[DEBUG] Got memAddrStr as [0x" + memAddrStr + "] or [" + str(memAddr) + "]"
    
    while(count < entryEnd):
        cmd = logCommandJSON['command'] + hex(memAddr)[2:]
        print ("Sending log entry command " + cmd + " to get entry #" + str(count) + " out of limit of " + str(entryEnd))
        recvString = connection.sendCommand(str(cmd))
        
        if memAddr == 0:
            memAddr = 511
        else:
            memAddr = memAddr - 1
            
        if recvString == "evno":
            break
        
        logEntryListStr.append(recvString[2:len(recvString)-3])
        
        count = count + 1
    
    index = 0
    
    for logStr in logEntryListStr:
        logEntry = makeLogListEntry(number = index+1)
        
        logEntry['code'] = logStr[0] + logStr[1] + logStr[2] + logStr[3]
        logEntry['event'] = CodeTable.getEventNameByCode(logEntry['code'])
        
        
        
        logEntryList.append(logEntry)
        index += 1
        
    
    
    return logEntryList
    
    
    
    