'''
Created on Feb 8, 2015

@author: rpavlyuk
'''

'''
TODO: Base direction auto configuration
'''
directoryBase = "/Users/rpavlyuk/Work/LifeSOS/PyLS30"

directoryConfig = "config"


fileCommandsConfig = "LS30Commands.json"


def getConfigFolder(bDir=""):
    global directoryBase
    
    if bDir != "":
        directoryBase = bDir
        
    return directoryBase + "/" + directoryConfig


def getCommandsConfig():
    global fileCommandsConfig
    return getConfigFolder() + "/" + fileCommandsConfig
    
    
