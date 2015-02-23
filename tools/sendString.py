#!/usr/bin/python
# encoding: utf-8


import sys
import os

dirBase = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, dirBase)

from LS30Connector import ReqRsnp
from LS30Util import Config

Config.setBaseDir(dirBase)


reqRsnp = ReqRsnp.ReqRsnp()

reqRsnp.sendRequest("!vn&", 99)
