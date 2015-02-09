'''
Created on Feb 9, 2015

@author: rpavlyuk
'''

from LS30Util import Config
import os.path

def getWEBTemlate(templateFile):
    
    templateFilePath = Config.getWEBTemplatesDir() + "/" + templateFile
    templateContent = ""
    
    
    if not os.path.isfile(templateFilePath):
        raise ValueError("Template %s not found in directory %s" % (templateFile, Config.getWEBTemplatesDir()))
    
    try:
        templateFile = open(templateFilePath)
        templateContent = templateFile.read()
        
    except:
        print "Unable to read file contents from file " + templateFilePath
    
    
    
    return templateContent




