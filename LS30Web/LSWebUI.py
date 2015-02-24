'''
Created on Feb 6, 2015

@author: rpavlyuk
'''

from bottle import Bottle, run, SimpleTemplate, static_file, redirect

from LS30Connector import ReqRsnp
from LS30Util import Commands, Config
from LS30Web import Util
from LS30Data import DeviceLog, DeviceStatus

import pprint

webHost = "localhost"
webPort = 8080

# connString  = "socket://192.168.1.220:1681"
connString  = Config.getLS30ConnectionString()

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
    SimpleTemplate.defaults["get_url"] = app.get_url
    reqRsnp = ReqRsnp.ReqRsnp(connString)       
    run(app, host=webHost, port=webPort)
    
@app.route('/', name='index')
def index():
    url = app.get_url('device_log', entryStart=0, entryEnd=10)
    redirect(url)
    
@app.route('/ls30/', name='index_ls30')
def index_ls30():
    url = app.get_url('device_log', entryStart=0, entryEnd=10)
    redirect(url)

@app.route('/ls30/static/:path#.+#', name='static')
def static(path):
    return static_file(path, root=Config.getWEBStaticContentDir())
 
@app.route('/ls30/serial/get/<command>')
def serial(command):  
    
    global reqRsnp
    
    print "Sending command to serial TCP port"
    response = reqRsnp.sendCommand(command)

    return response

@app.route('/ls30/command/send/<command>')
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

@app.route('/ls30/display/log/<entryStart>/<entryEnd>', name='device_log')
def displayLog(entryStart=0, entryEnd=25):
    
    global reqRsnp
    
    templateFileName = "displayLogEntries.html"
    
    tpl = SimpleTemplate(Util.getWEBTemlate(templateFileName))
    
    totalEventCount = DeviceLog.getTotalEventsCount(reqRsnp)
    eventList = DeviceLog.getDeviceLog(reqRsnp, int(entryStart), int(entryEnd))
    
    # pagination
    eventsOnPage = int(entryEnd) - int(entryStart)
    pagesCount = int(totalEventCount) / eventsOnPage
    if int(totalEventCount)%eventsOnPage > 0:
        pagesCount = pagesCount + 1
    i = 1
    pageList = [ ]
    while(i <= pagesCount):
        if (int(entryStart) == (i-1)*eventsOnPage):
            actual = 1
        else:
            actual = 0
        pageItem = {'actual' : actual, 'number' : i, 'entryStart' : (i-1)*eventsOnPage, 'entryEnd' : i*eventsOnPage if (i*eventsOnPage < int(totalEventCount)) else int(totalEventCount) }
        pageList.append(pageItem)
        i += 1
    
    return tpl.render(eventList=eventList, totalEventCount=totalEventCount, entryStart=entryStart, entryEnd=entryEnd, pageList=pageList, pageTitle="Events Log")

@app.route('/ls30/display/devices/<deviceGroup>', name='device')
def displayDevices(deviceGroup):
    
    global reqRsnp

    templateFileName = "displayDevices.html"
    
    tpl = SimpleTemplate(Util.getWEBTemlate(templateFileName))
       
    deviceList = DeviceStatus.getDeviceStatus(reqRsnp, int(deviceGroup))
    
    return tpl.render(deviceList=deviceList, pageTitle="Devices")
    

    
    
    
    
    
    
    


        