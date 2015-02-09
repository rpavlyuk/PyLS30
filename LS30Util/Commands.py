'''
Created on Feb 8, 2015

@author: rpavlyuk
'''

import json
from LS30Util import Config
from pprint import pprint

commandsDataJSON = ""

isJSONLoaded = False

def loadCommandsFromFile(commandsJSONFile=""):
    
    global commandsDataJSON
    global isJSONLoaded
    
    if commandsJSONFile == "":
        commandsJSONFile=Config.getCommandsConfig()
        
    commandsData=open(commandsJSONFile)
    
    commandsDataJSON = json.load(commandsData)
    
    isJSONLoaded = True
    
    commandsData.close()
    
    

def printCommandsData2StdOut(data=""):
    
    global commandsDataJSON
    
    if data == "":
        pprint(commandsDataJSON)
    else:
        pprint(data)
        
        
def getCommandJSON(commandPath):
    global commandsDataJSON
    global isJSONLoaded

    commandJSON = commandsDataJSON
    
    if not isJSONLoaded:
        print "[WARNING] JSON command data were not loaded!"
        return commandJSON
    
    print "Looking for JSON object in commands file by search path [" + commandPath + "]"
    
    jsonIndex = ""
    
    while(True):
       
        try:
            # get the value until first found dot
            jsonIndex = commandPath[:commandPath.index(".")]
            if jsonIndex == "":
                break
            # remove everything until including first found dot
            commandPath = commandPath[commandPath.index(".")+1:]
        except ValueError:
            jsonIndex = commandPath
        

        print "[DEBUG] First index is " + jsonIndex
        
        if isinstance(commandJSON, list):
            print "[DEBUG] So, we have a list here..."
            for command in commandJSON:
                if command['id'] == jsonIndex:
                    print "[DEBUG] Found list entry " + jsonIndex
                    commandJSON = command
                    break
        else:
            commandJSON = commandJSON[jsonIndex]
        
        print "[DEBUG] JSON Object under index " + jsonIndex + " is:"
        pprint(commandJSON)
        
        if jsonIndex == commandPath:
            break
        
    
    return commandJSON

