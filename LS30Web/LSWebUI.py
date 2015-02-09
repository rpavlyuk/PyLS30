'''
Created on Feb 6, 2015

@author: rpavlyuk
'''

from bottle import Bottle, run, SimpleTemplate

from LS30Connector import ReqRsnp
from LS30Util import Commands, Config
from LS30Web import Util
from LS30Data import DeviceLog

import pprint

webHost = "localhost"
webPort = 8080

# connString  = "socket://192.168.1.220:1681"
connString  = "socket://home.pavlyuk.lviv.ua:1681"

app = Bottle()
isInitialized = False

reqRsnp = None


def init(host="localhost", port=8080):
    global webHost, webPort, isInitialized
    webHost = host
    webPort = port
    isInitialized = True
    

def start():
    global reqRsnp, webHost, webPort
    reqRsnp = ReqRsnp.ReqRsnp(connString)       
    run(app, host=webHost, port=webPort)
    

@app.route('/hello')
def hello():
    return "Hello World!"
 
@app.route('/serial/get/<command>')
def serial(command):  
    
    global reqRsnp
    
    print "Sending command to serial TCP port"
    response = reqRsnp.sendCommand(command)

    return response

@app.route('/command/send/<command>')
def commandSend(command):
    global reqRsnp

    Commands.loadCommandsFromFile()
    jsonCommand = Commands.getCommandJSON(command)
    lsResponse = reqRsnp.sendCommand(str(jsonCommand['command']))
   
    response = "<p><strong>Got command id:</p></strong><pre>"+command+"</pre>"
    
    response += '<p><strong>Found command definition in JSON configuration file:</p></strong><div style="width:400px;"><pre>'
    response += pprint.pformat(jsonCommand)
    response += '</pre></div>'
    
    response += '<p><strong>Got response from LS-30 ('+reqRsnp.connString+'):</p></strong><div style="width:400px;"><pre>'
    response += lsResponse
    response += '</pre></div>'
    
    return response

@app.route('/display/log/<entryStart>/<entryEnd>')
def displayLog(entryStart=0, entryEnd=25):
    
    templateFileName = "displayLogEntries.html"
    templateFilePath = Config.getWEBTemplatesDir() + "/" + templateFileName
    
    tpl = SimpleTemplate(Util.getWEBTemlate(templateFileName))
    
    eventList = DeviceLog.getDeviceLog(entryStart, entryEnd)
    
    return tpl.render(eventList=eventList)
    
    
    
    
    
    


        