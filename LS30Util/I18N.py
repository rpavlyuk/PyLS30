'''
Created on Feb 26, 2015

@author: rpavlyuk
'''

from LS30Util import Config

import json


def getString(fileName, label):   
    file = open(fileName)  
    return json.load(file)[str(label)]

def getHelpString(label):
    fileName = Config.getStringsFileHelp()
    return getString(fileName, label)
