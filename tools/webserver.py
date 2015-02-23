#!/usr/bin/python
# encoding: utf-8
'''
Created on Feb 6, 2015

@author: rpavlyuk
'''
import sys
import os

dirBase = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, dirBase)

from LS30Web import LSWebUI
from LS30Util import Config

Config.setBaseDir(dirBase)
Config.configure()


if __name__ == '__main__':
    LSWebUI.start()
