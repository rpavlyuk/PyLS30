'''
Created on Feb 6, 2015

@author: rpavlyuk
'''
from serial import serial_for_url, SerialException
from lib2to3.fixer_util import String


class ReqRsnp():
    '''
    classdocs
    '''
    
    connection = None

    connString  = "socket://home.pavlyuk.lviv.ua:1681"
    # connString  = "socket://192.168.1.220:1681"
    
    read_limit = 4096
    
    
    cmd_prefix = "!"
    cmd_suffix = "&"
    
    '''
    Do debug logging?
    '''
    doConnDebug = True
    
    
    '''
    Both request and response appear in the serial thread. We'd like to stop reading the response once
    we hit "&" symbol but it might happen that this will be the request itself. So, we need to stop at 
    second "&"
    '''
    cmd_EoC_count = 1

    def __init__(self, connectionString = ""):
        '''
        Constructor.
        
        Opens connection to the remote serial-to-TCP port specified by connectionString
        '''
        if connectionString != "":
            self.connString = connectionString
        
        print "Opening serial connection to " + self.connString
        self.connection = serial_for_url(self.connString)
        
        if not self.connection.isOpen():
            raise SerialException()
        
        print "Connection to "+ self.connString + " established"
    

    def sendRequest(self, requestString, chunkSize=1):
        '''
        Send raw text to serial port
        ''' 
        
        print "Port opened. Sending request '" + requestString + "'"
        self.connection.write(requestString)
        
        resp = ""
        msg = ""
        index = 0
        eoc_index = 1
        
        print "Reading port output"
        while (index < self.read_limit):
            msg = self.connection.read(chunkSize)
            if self.doConnDebug:
                print "[DEBUG] Got chunk [" + str(index) + "]: " + msg
            resp += msg
            if msg == "&":
                if self.doConnDebug:
                    print "[DEBUG] Got symbol & as a chunk for " + str(eoc_index) + " time!"
                if eoc_index >= self.cmd_EoC_count:
                    break
                eoc_index += 1
            index+=1
        
        print "Got response: " + resp
        if self.read_limit-1 == index:
            print "WARNING: Read length was reached ("+self.read_limit+")"
        
        return resp
    
    def sendCommand(self, command, extractResponse = True):
        '''
        Sends LS-like command to BF-450 TCP-to-Serial port
        '''
        
        cmd = self.cmd_prefix + command + self.cmd_suffix
        
        if extractResponse:
            return self.extractResponse(self.sendRequest(cmd))
        else:
            return self.sendRequest(cmd)
    
    def extractResponse(self, lsSerialResponse):
        '''
        Extract the response message from raw LS30 serial response
        '''
        
        message = ""
        
        try:
            message = lsSerialResponse[lsSerialResponse.index(self.cmd_prefix)+1:lsSerialResponse.index(self.cmd_suffix)]
        except ValueError:
            print "Unable to extract command from response ["+lsSerialResponse+"]"
        
        
        return message
        
            
        