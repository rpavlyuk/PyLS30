#!/usr/bin/python
# encoding: utf-8


import sys
import os
sys.path.insert(0, "/Users/rpavlyuk/Work/LifeSOS/PyLS30")
from LS30Connector import ReqRsnp



reqRsnp = ReqRsnp.ReqRsnp()

reqRsnp.sendRequest("!vn&", 99)
