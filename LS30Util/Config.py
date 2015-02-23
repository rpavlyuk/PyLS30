'''
Created on Feb 8, 2015

@author: rpavlyuk
'''

import logging

'''
Configuration flag
'''
isConfigured = False

'''
Basic settings
'''
logLevel = logging.DEBUG

'''
Base directory where all PyLS30 libraries and files reside
'''
directoryBase = "./"


'''
Directories and files
'''
directoryConfig = "config"
directoryWebTemplates = "templates/web"
directoryCodeTable = "code"

fileCommandsConfig = "LS30Commands.json"
fileEventCode = "eventCode.json"
fileEventTypeCode = "eventTypeCode.json"
fileHexCode = "Hex.json"
fileRHexCode = "RHex.json"

'''
Remote access settings
'''
# ls30_socket_url = "socket://192.168.1.220:1681"
ls30_socket_url = "socket://home.pavlyuk.lviv.ua:1681"


'''
Routines
'''
def configure():
    global isConfigured, logLevel  
    
    if isConfigured:
        return
    
    logging.basicConfig(level=logLevel)
    


def getConfigFolder(bDir=""):
    global directoryBase
    
    if bDir != "":
        directoryBase = bDir
        
    return directoryBase + "/" + directoryConfig

def setBaseDir(baseDir):
    global directoryBase
    directoryBase = baseDir  

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

def getCodeTableEventTypes():
    global fileEventTypeCode
    return getCodeTableConfigDirectory() + "/" + fileEventTypeCode

def getCodeTableHex():
    global fileHexCode
    return getCodeTableConfigDirectory() + "/" + fileHexCode

def getCodeTableRHex():
    global fileHexCode
    return getCodeTableConfigDirectory() + "/" + fileRHexCode
    


    
