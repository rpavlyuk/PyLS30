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




def getDeviceStatus(connection, deviceGroup = 0, countStart = 0):
    
    deviceLimit = 256
    
    listDevices = [ ]
    listDevicesStr = [ ]
    
    recvString = ""
    
    sGroup = None
    
    Config.getLogger().debug("Getting device group information")
    deviceGroup = int(deviceGroup)    
    deviceGroups = CodeTable.getSensorGroupConfig() 
    
    Config.getLogger().debug("Loaded device groups:\n %s", pformat(deviceGroups))
    
    if int(deviceGroup) < len(deviceGroups['sensorGroups']):    
        for sensorGroup in deviceGroups['sensorGroups']:
            if sensorGroup['id'] == deviceGroup:
                sGroup = sensorGroup
                break
        
        if not sGroup:
            raise ValueError("Incorrect deviceGroup variable provided")
    else:
        # it means that we are going to get all devices.
        # We will use recursion for this purpose
        
        Config.getLogger().info("Getting all devices by iterating over sensor groups")
        
        countStart = 1
        
        for sensorGroup in deviceGroups['sensorGroups']:
            
            Config.getLogger().debug("Got sensor group: " + pformat(sensorGroup))
            
            deviceGroupList = getDeviceStatus(connection, int(sensorGroup['id']), countStart-1)
            countStart += len(deviceGroupList)
            
            listDevices.extend(deviceGroupList)
            
        return listDevices
            
            
    
    count = 0
    
    Commands.loadCommandsFromFile()
    deviceCommandJSON = Commands.getCommandJSON(sGroup['command'])
    
    while (count < deviceLimit):
        cmd = deviceCommandJSON['command'] + "?" + Common.hex2_encoded(count)[2:]
        Config.getLogger().debug("Sending device status command " + str(cmd) + " for device #" + str(count))
        recvString = connection.sendCommand(str(cmd))
        
        if (recvString[2]+recvString[3] == "00"):
            break
        
        if (recvString == deviceCommandJSON['command'] + "no"):
            break
        
        listDevicesStr.append(recvString[2:])
        count += 1
    
    Config.getLogger().debug("List of event strings:\n %s", pformat(listDevicesStr))
    
    index = countStart
    
    for deviceString in listDevicesStr:
        
        device = makeDeviceEntry(index+1)
        
        device['zone'] = deviceString[14] + deviceString[15] + "-" + deviceString[16] + deviceString[17]
        device['sensorType'] = CodeTable.getSensorTypeByCode(deviceString[0] + deviceString[1])
        device['sensorId'] = deviceString[2] + deviceString[3] + deviceString[4] + deviceString[5] + deviceString[6]
        device['ma'] = deviceString[8] + deviceString[9]
        device['dc'] = deviceString[10] + deviceString[11]
        device['es'] = deviceString[18] + deviceString[19] + deviceString[20] + deviceString[21]
        device['x10'] = deviceString[22] + deviceString[23] + deviceString[24] + deviceString[25]
        device['cs'] = deviceString[26] + deviceString[27]
        device['dt'] = deviceString[28] + deviceString[29]
        
        if (len(deviceString) > 30):
            device['cd'] = str(0 - (255 - int(deviceString[30] + deviceString[31],16) + 1))
            if device['cd'] == "-128":
                device['cd'] = ""
            device['hl'] = str(0 - (255 - int(deviceString[32] + deviceString[33],16) + 1))
            if device['hl'] == "-128":
                device['hl'] = ""
            device['ll'] = str(0 - (255 - int(deviceString[34] + deviceString[35],16) + 1))
            if device['ll'] == "-128":
                device['ll'] = ""
            device['ss'] = deviceString[36] + deviceString[37]
            
        
        listDevices.append(device)
        index += 1
        
        
    
    
    
    return listDevices