'''
Created on Feb 6, 2015

@author: rpavlyuk
'''

from bottle import Bottle, run

from LS30Connector import ReqRsnp

webHost = "localhost"
webPort = 8080

connString  = "socket://192.168.1.220:1681"

app = Bottle()
isInitialized = False

def init(host="localhost", port=8080):
    webHost = host
    webPort = port
    isInitialized = True
    

def start():
    run(app, host=webHost, port=webPort)

@app.route('/hello')
def hello():
     return "Hello World!"
 
@app.route('/serial/get/<command>')
def serial(command):
    
    reqRsnp = ReqRsnp.ReqRsnp(connString)
    
    print "Sending command to serial TCP port"
    response = reqRsnp.sendCommand(command)

    return response


        