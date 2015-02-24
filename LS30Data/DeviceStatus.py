'''
Created on Feb 24, 2015

@author: rpavlyuk
'''
from LS30Util import Commands, Common, Config
from LS30Data import CodeTable

from pprint import pformat

def makeDeviceEntry(number=0, zone="", sensorType="", sensorId="", ma="", dc="", es="", x10="", cs="", dt="", cd="", hl="", ll="", ss="", deviceName=""):
    
    return {'number': number, 'zone': zone, 'sensorType' : sensorType, 'sensorId': sensorId, 'ma' : ma, 
            'dc' : dc, 'es': es, 'x10' : x10, 'cs' : cs, 'dt' : dt, 'cd' : cd, 'hl' : hl, 'll' : ll, 'ss' : ss, 'deviceName' : deviceName}




def getDeviceStatus(connection, deviceGroup = 0):
    
    deviceLimit = 256
    
    listDevices = [ ]
    listDevicesStr = [ ]
    
    recvString = ""
    
    sGroup = None
    
    Config.getLogger().debug("Getting device group information for id " + str(deviceGroup))
    deviceGroup = int(deviceGroup)    
    deviceGroups = CodeTable.getSensorGroupConfig() 
    
    Config.getLogger().debug("Loaded device groups:\n %s", pformat(deviceGroups))
    
    for sensorGroup in deviceGroups['sensorGroups']:
        if sensorGroup['id'] == deviceGroup:
            sGroup = sensorGroup
            break
    
    if not sGroup:
        raise ValueError("Incorrect deviceGroup variable provided")
    
    count = 0
    
    Commands.loadCommandsFromFile()
    deviceCommandJSON = Commands.getCommandJSON(sGroup['command'])
    
    while (count < deviceLimit):
        cmd = deviceCommandJSON['command'] + Common.hex2_encoded(count)[2:]
        Config.getLogger().debug("Sending device status command " + str(cmd) + " for device #" + str(count))
        recvString = connection.sendCommand(str(cmd))
        
        if (recvString[2]+recvString[3] == "00"):
            break
        
        if (recvString == deviceCommandJSON['command'] + "no"):
            break
        
        listDevicesStr.append(recvString[2:])
        count += 1
    
    Config.getLogger().debug("List of event strings:\n %s", pformat(listDevicesStr))
    
    return listDevices