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
logger = None
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
directoryWebStaticContent = "content/web/static"
directoryCodeTable = "code"
directoryLog = "log"

fileMainLog = "main.log"
fileCommandsConfig = "LS30Commands.json"
fileSensorGroupsConfig = "LS30SensorGroups.json"
fileEventCode = "eventCode.json"
fileEventTypeCode = "eventTypeCode.json"
fileHexCode = "Hex.json"
fileRHexCode = "RHex.json"

'''
Remote access settings
'''
#ls30_socket_url = "socket://192.168.1.220:1681"
ls30_socket_url = "socket://home.pavlyuk.lviv.ua:1681"


'''
Routines
'''
def configure():
    global isConfigured, logLevel, logger
    
    # if we're configured then nothing to do here
    if isConfigured:
        return
    
    # let's create an instance of logger object
    logger = logging.getLogger('PyLS30')
    logger.setLevel(logLevel)
    
    # We'd like to log into both file and console so
    # first we create a log file handler
    fh = logging.FileHandler(getMainLogFile())
    fh.setLevel(logLevel)
    
    # ... then console handler
    ch = logging.StreamHandler()
    ch.setLevel(logLevel)
    
    # We'd like file logging to be nice
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    
    # Now let's add the handlers to the logger object  
    logger.addHandler(fh)
    logger.addHandler(ch)
    
    # Let's configure global system logging, just in case some dude decided to use it
    # instead of our configured one
    logging.basicConfig(level=logLevel)
    
    isConfigured = True
    
def getLogger():
    global logger
    return logger


def getConfigFolder(bDir=""):
    global directoryBase
    
    if bDir != "":
        directoryBase = bDir
        
    return directoryBase + "/" + directoryConfig

def setBaseDir(baseDir):
    global directoryBase
    directoryBase = baseDir
    
def getBaseDirectory():
    global directoryBase
    return directoryBase  

def getCommandsConfig():
    global fileCommandsConfig
    return getConfigFolder() + "/" + fileCommandsConfig

def getWEBTemplatesDir():
    global directoryBase, directoryWebTemplates    
    return directoryBase + "/" + directoryWebTemplates

def getWEBStaticContentDir():
    global directoryWebStaticContent
    return getBaseDirectory() + "/" + directoryWebStaticContent

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

def getLogDirectory():
    global directoryLog
    return getBaseDirectory() + "/" + directoryLog

def getMainLogFile():
    global fileMainLog
    return getLogDirectory() + "/" + fileMainLog

def getSensorGroupConfig():
    global fileSensorGroupsConfig
    return getConfigFolder() + "/" + fileSensorGroupsConfig
    


    
