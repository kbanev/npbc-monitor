#!/usr/bin/python

import serial
import time
import multiprocessing
import settings
import sqlite3
import npbc_communication
import binascii


class SerialProcessSet(multiprocessing.Process):
    def __init__(self, Mode, Priority):
        multiprocessing.Process.__init__(self)
        self.__Mode=Mode
        self.__Priority=Priority
		
    def run(self):
        sp = serial.Serial(settings.SERIAL_PORT, settings.SERIAL_BAUDRATE, timeout=1)
        print ("communicating on port: " + sp.portstr)
        if (sp.isOpen()):
            try:
                time.sleep(0.1)
                sp.flushInput()
                sp.flushOutput()
                time.sleep(0.1)
                requestData = npbc_communication.setModeAndPriorityCommand(self.__Mode,self.__Priority).getRequestData()
                #requestData = [0x5A, 0x5A, 0x03, 0x07, 0x47, 0xB1]
                print(requestData)
                sp.write(requestData)
                responseData=""
        
                time.sleep(0.5)
                if (sp.in_waiting > 0):
                    responseData = bytearray(sp.read(sp.in_waiting))
                    print(responseData)
                else:
                    print(sp.in_waiting)
		
                if (len(responseData) > 0):
                    response = npbc_communication.setModeAndPriorityCommand(self.__Mode,self.__Priority).processResponseData(responseData)
        
                    if (isinstance(response, npbc_communication.failResponse)):
                        print( "   -> failed")
        
                    if (isinstance(response, npbc_communication.successResponse)):
                        print( "   -> success")
                    else:
                        print( "   -> failed")
                else:
                    print( "   -> failed in response data")
            
            except Exception as e1:
                print ("error communicating...: " + str(e1))
				