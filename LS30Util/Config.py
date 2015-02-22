'''
Created on Feb 8, 2015

@author: rpavlyuk
'''

'''
TODO: Base directory auto configuration
'''
directoryBase = "/Users/rpavlyuk/Work/LifeSOS/PyLS30"


'''
Directories and files
'''
directoryConfig = "config"
directoryWebTemplates = "templates/web"
directoryCodeTable = "code"

fileCommandsConfig = "LS30Commands.json"
fileEventCode = "eventCode.json"

'''
Remote access settings
'''
ls30_socket_url = "socket://192.168.1.220:1681"



'''
Routines
'''

def getConfigFolder(bDir=""):
    global directoryBase
    
    if bDir != "":
        directoryBase = bDir
        
    return directoryBase + "/" + directoryConfig


def getCommandsConfig():
    global fileCommandsConfig
    return getConfigFolder() + "/" + fileCommandsConfig

def getWEBTemplatesDir():
    global directoryBase, directoryWebTemplates    
    return directoryBase + "/" + directoryWebTemplates


def getLS30ConnectionString():
    global ls30_socket_url
    return ls30_socket_url 

def getCodeTableConfigDirectory():
    global directoryCodeTable
    return getConfigFolder() + "/" + directoryCodeTable

def getCodeTableEvents():
    global fileEventCode
    return getCodeTableConfigDirectory() + "/" + fileEventCode
    
