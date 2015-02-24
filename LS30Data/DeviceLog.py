'''
Created on Feb 9, 2015

@author: rpavlyuk
'''

from LS30Util import Commands, Common, Config
from LS30Data import CodeTable
from pprint import pformat
import time
import datetime


eventCommandPath = "commands.spec_commands.event"

this_year = None
this_month = None


def makeLogListEntry(number=0, code="", event="None", zone="", event_type="", activated="", date="", time="", device_name="", timestamp=""):
    
    logEntry =  {"number": number, "code": code, "event": event, "zone": zone, "event_type": event_type, "activated": activated, "date": date, "time": time, "device_name": device_name, "timestamp": timestamp}     
    return logEntry


def parseDateTime(dateTimeString="00000000"):
    global this_month, this_year
    mm = int(dateTimeString[0] + dateTimeString[1])
    dd = int(dateTimeString[2] + dateTimeString[3])
    hh = int(dateTimeString[4] + dateTimeString[5])
    mn = int(dateTimeString[6] + dateTimeString[7])
        
    if not this_year:
        this_year = int(time.strftime("%Y"))
        this_month = int(time.strftime("%m"))
    
    year = 0  
      
    if mm > this_month:
        year = this_year - 1
    else:
        year = this_year
    
    logDateTime = datetime.datetime(year, mm, dd, hh, mn, 0)
    
    return logDateTime
    
    
'''
Get total number of events.

Arguments:
    <connection>    A ReqRspn object with initialized connection to LS-30
'''   
def getTotalEventsCount(connection):

    global eventCommandPath
    
    Commands.loadCommandsFromFile()
    
    logCommandJSON = Commands.getCommandJSON(eventCommandPath)
 
    recvString = connection.sendCommand(str(logCommandJSON['command'] + "000"))
    memAddrStr = recvString[len(recvString)-3:]
    memAddr = int(memAddrStr, 16)   
    
    Config.getLogger().debug("Got memAddrStr as [0x" + memAddrStr + "] or [" + str(memAddr) + "]")
    
    return memAddr


'''
Get device log entries in a form of list. Requires serial connection as a mandatory argument.

Arguments:
    <connection>    A ReqRspn object with initialized connection to LS-30
    <entryStart>    (int) Starting entry of the log file to be returned
    <entryEnd>      (int) Last entry of LS-30 log to be returned
    
Returns:
    (list) Log entries list
'''
def getDeviceLog(connection, entryStart=0, entryEnd=25):
    
    global eventCommandPath
    
    count = int(entryStart)
    
    logEntryListStr = [ ]
    
    logEntryList = [  ]
    
    Commands.loadCommandsFromFile()
    
    logCommandJSON = Commands.getCommandJSON(eventCommandPath)

    memAddr = getTotalEventsCount(connection) - int(entryStart)
    
    while(count <= entryEnd):
        cmd = logCommandJSON['command'] + Common.hex3_encoded(memAddr)[2:]
        # cmd = logCommandJSON['command'] + Common.hex3(count)[2:]
        Config.getLogger().debug("Sending log entry command " + cmd + " to get entry #" + str(count) + " out of limit of " + str(entryEnd))
        recvString = connection.sendCommand(str(cmd))
        
        if memAddr == 0:
            memAddr = 511
        else:
            memAddr = memAddr - 1
            
        if recvString == "evno":
            break
        
        logEntryListStr.append(recvString[2:len(recvString)-3])
        
        count = count + 1
    
    index = entryStart
    
    Config.getLogger().debug("List of event strings:\n %s", pformat(logEntryListStr))
    
    for logStr in logEntryListStr:
        logEntry = makeLogListEntry(number = index)
        
        logEntry['code'] = logStr[0] + logStr[1] + logStr[2] + logStr[3]
        logEntry['event'] = CodeTable.getEventNameByCode(logEntry['code'])
        logEntry['zone'] = logStr[4] + logStr[5] + "-" + logStr[8] + logStr[9]
        logEntry['event_type'] = CodeTable.getEventTypeByCode(logStr[7]) 
        logEntry['activated'] = logStr[10] + logStr[11]
        logEntry['timestamp'] = parseDateTime(logStr[12] + logStr[13] + logStr[14] + logStr[15] + logStr[16] + logStr[17] + logStr[18] + logStr[19])        
        logEntry['date'] = '{:%Y-%m-%d, %a}'.format(logEntry['timestamp'])
        logEntry['time'] = '{:%H:%M:%S}'.format(logEntry['timestamp'])
        
        logEntryList.append(logEntry)
        index += 1
          
    
    return logEntryList
    
    
    
    