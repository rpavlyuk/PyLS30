#!/usr/bin/python
# encoding: utf-8
'''
Created on Feb 6, 2015

@author: rpavlyuk
'''
import sys
import os
sys.path.insert(0, "/Users/rpavlyuk/Work/LifeSOS/PyLS30")
from LS30Web import LSWebUI
from bottle import Bottle, run


if __name__ == '__main__':
    LSWebUI.start()
