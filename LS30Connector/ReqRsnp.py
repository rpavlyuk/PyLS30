'''
Created on Feb 6, 2015

@author: rpavlyuk
'''
from serial import serial_for_url, SerialException
import logging

from LS30Util import Config
from serial.serialutil import portNotOpenError


class ReqRsnp():
    '''
    classdocs
    '''
    
    connection = None
    
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
        else:
            self.connString = Config.getLS30ConnectionString()
        
        Config.getLogger().info("Opening serial connection to " + self.connString)
        self.connection = serial_for_url(self.connString)
        
        if not self.connection.isOpen():
            raise SerialException()
        
        Config.getLogger().info("Connection to "+ self.connString + " established")
    
    
    def __del__ (self):
        '''
        Destructor
        
        Makes sure that connection was closed before object is deleted
        '''
        if self.connection.isOpen:
            self.connection.close()
        
        if not self.connection.isOpen():
            Config.getLogger().info("Connection closed successfully")
    
    def resetConnection(self):
        
        connCheckIterations = 2048
        i = 0
        
        Config.getLogger().debug("Performing Serial-over-TCP connection reset")
        
        self.connection.close()
        
        if self.connection.isOpen:
            Config.getLogger().error("Unable to close connection to " + self.connString)
        
        self.connection.open()
        
        while(i < connCheckIterations):
            if self.connection.isOpen:
                Config.getLogger().debug("Connection became ready after " + str(i) + " iterations")
                break
            i+=1
        
        if not self.connection.isOpen:
            Config.getLogger().error("Unable to open connection to " + self.connString)
    

    def sendRequest(self, requestString, chunkSize=1):
        '''
        Send raw text to serial port
        ''' 
        
        Config.getLogger().debug("Port opened. Sending request '" + requestString + "'")
        self.resetConnection()
        self.connection.write(requestString)
        
        resp = ""
        msg = ""
        index = 0
        eoc_index = 1
        
        Config.getLogger().debug("Reading port output")
        while (index < self.read_limit):
            msg = self.connection.read(chunkSize)
            # Config.getLogger().debug("Got chunk [" + str(index) + "]: " + msg)
            resp += msg
            if msg == "&":
                # Config.getLogger().debug("Got symbol & as a chunk for " + str(eoc_index) + " time!")
                if eoc_index >= self.cmd_EoC_count:
                    break
                eoc_index += 1
            index+=1
        
        Config.getLogger().debug("Got response: " + resp)
        if self.read_limit-1 == index:
            Config.getLogger().warning("Read length was reached ("+self.read_limit+")")
        
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
            Config.getLogger().error("Unable to extract command from response ["+lsSerialResponse+"]")
        
        
        return message
        
            
        