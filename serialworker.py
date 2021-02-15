#!/usr/bin/python

import serial
import time
import multiprocessing
import settings
import sqlite3
import npbc_communication
import binascii
import random

class SerialProcess(multiprocessing.Process):
    def __init__(self):
        multiprocessing.Process.__init__(self)
        self.testGIResponses = [[0x5A, 0x5A, 0x1D, 0x16, 0x14, 0x12, 0x4B, 0x57, 0x1B, 0x18, 0x1D, 0x09, 0x09, 0x0A, 0x0B, 0x8C,
                                    0x0D, 0x0E, 0x0F, 0x4C, 0x46, 0x92, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x99, 0x1A, 0x1B, 0xFA],
                                [0x5A, 0x5A, 0x1D, 0x16, 0x14, 0x12, 0x4B, 0x5C, 0x1B, 0x18, 0x1D, 0x09, 0x09, 0x0A, 0x0B, 0x8C,
                                    0x0D, 0x0E, 0x0F, 0x4C, 0x47, 0x92, 0x13, 0x14, 0x1D, 0x16, 0x17, 0x18, 0x99, 0x1A, 0x1B, 0xEC],
                                [0x5A, 0x5A, 0x1D, 0x16, 0x14, 0x12, 0x4C, 0x27, 0x1B, 0x18, 0x1D, 0x09, 0x09, 0x0A, 0x0B, 0x8C,
                                    0x0D, 0x0E, 0x0F, 0x4C, 0x46, 0x92, 0x13, 0x14, 0x1D, 0x16, 0x17, 0x18, 0x99, 0x1A, 0x1B, 0x21],
                                [0x5A, 0x5A, 0x1D, 0x16, 0x14, 0x12, 0x4C, 0x5C, 0x1B, 0x18, 0x1D, 0x09, 0x09, 0x0B, 0x0B, 0x8C,
                                    0x0D, 0x0E, 0x0F, 0x4C, 0x46, 0x92, 0x13, 0x14, 0x2D, 0x16, 0x7B, 0x18, 0x19, 0x1A, 0x1B, 0xF7],
                                [0x5A, 0x5A, 0x1D, 0x16, 0x14, 0x12, 0x53, 0x07, 0x1B, 0x18, 0x1D, 0x09, 0x09, 0x0D, 0x0B, 0x8C,
                                    0x0D, 0x0E, 0x0F, 0x4C, 0x46, 0x92, 0x13, 0x14, 0x1D, 0x16, 0x17, 0x18, 0x19, 0x1A, 0x1B, 0xB7],
                                [0x5A, 0x5A, 0x1D, 0x16, 0x14, 0x12, 0x53, 0x0C, 0x1B, 0x18, 0x1D, 0x09, 0x09, 0x0E, 0x0B, 0x8C,
                                    0x0D, 0x0E, 0x0F, 0x4C, 0x46, 0x92, 0x13, 0x14, 0x4D, 0x16, 0x17, 0x18, 0x19, 0x1A, 0x1F, 0x7D],
                                [0x5A, 0x5A, 0x1D, 0x16, 0x14, 0x13, 0x05, 0x57, 0x1B, 0x18, 0x1D, 0x09, 0x09, 0x13, 0x0B, 0x8C,
                                    0x0D, 0x0E, 0x0F, 0x4C, 0x49, 0x92, 0x93, 0xB2, 0x1D, 0x16, 0x42, 0x1C, 0x19, 0x1A, 0x1B, 0x5E],
                                [0x5A, 0x5A, 0x1D, 0x16, 0x14, 0x13, 0x05, 0x5C, 0x1B, 0x18, 0x1D, 0x09, 0x09, 0x13, 0x0B, 0x8C,
                                    0x0D, 0x0E, 0x0F, 0x4C, 0x4A, 0x92, 0x93, 0xB1, 0x1D, 0x16, 0x40, 0x1B, 0x19, 0x1A, 0x1B, 0x5C],
                                [0x5A, 0x5A, 0x1D, 0x16, 0x14, 0x12, 0x55, 0x47, 0x1B, 0x18, 0x1D, 0x09, 0x09, 0x10, 0x0B, 0x8C,
                                    0x0D, 0x0E, 0x0F, 0x4C, 0x46, 0x92, 0x93, 0xA1, 0x17, 0x16, 0x3E, 0x18, 0x19, 0x1A, 0x1B, 0x44],
                                [0x5A, 0x5A, 0x1D, 0x16, 0x14, 0x12, 0x55, 0x4C, 0x1B, 0x18, 0x1D, 0x09, 0x09, 0x12, 0x0B, 0x8C,
                                    0x0D, 0x0E, 0x0F, 0x4C, 0x46, 0x92, 0x93, 0xAC, 0x15, 0x16, 0x41, 0x18, 0x19, 0x1A, 0x1B, 0x31],
                                [0x5A, 0x5A, 0x1D, 0x16, 0x14, 0x12, 0x55, 0x4C, 0x1B, 0x18, 0x1D, 0x09, 0x09, 0x12, 0x0B, 0x8C,
                                    0x00, 0x00, 0x0F, 0x4C, 0x46, 0x92, 0x93, 0xAC, 0x15, 0x16, 0x41, 0x18, 0x19, 0x1A, 0x1B, 0x31]]

        self.testresetFFWorkTimeCounterCommandResponse = [0x5A, 0x5A, 0x02, 0x34, 0xCA]

    def run(self):
        sp = serial.Serial(settings.SERIAL_PORT, settings.SERIAL_BAUDRATE, timeout=1)
        print ("communicating on port: " + sp.portstr)

        dbconn = sqlite3.connect(settings.DATABASE)

        #responseData = bytearray(random.choice(self.testGIResponses))
        #n = 0

        while (sp.isOpen()):
            #n = n + 1
            #if (n > 12):
            #    responseData = bytearray(random.choice(self.testGIResponses))
            #    n = 0

            #resetFFWorkTimeCounterCommandResponseData = bytearray(self.testresetFFWorkTimeCounterCommandResponse)

            try:
                print ("exec: generalInformationCommand()")

                time.sleep(0.1)
                sp.flushInput()
                sp.flushOutput()

                time.sleep(0.1)
                requestData = npbc_communication.generalInformationCommand().getRequestData()
                sp.write(requestData)

                time.sleep(0.5)
                if (sp.inWaiting() > 0):
                    responseData = bytearray(sp.read(sp.inWaiting()))

                if (len(responseData) > 0):
                    response = npbc_communication.generalInformationCommand().processResponseData(responseData)

                    if (isinstance(response, npbc_communication.failResponse)):
                        print( "   -> failed")

                    if (isinstance(response, npbc_communication.generalInformationResponse)):
                        print( "   -> success")

                        if (response.FFWorkTime > 0):
                            print ("exec: resetFFWorkTimeCounterCommand()")

                            time.sleep(0.1)
                            sp.flushInput()
                            sp.flushOutput()

                            time.sleep(0.1)
                            resetFFWorkTimeCounterCommandRequestData = npbc_communication.resetFFWorkTimeCounterCommand().getRequestData()
                            sp.write(resetFFWorkTimeCounterCommandRequestData)

                            time.sleep(0.5)
                            if (sp.in_waiting > 0):
                                resetFFWorkTimeCounterCommandResponseData = bytearray(sp.read(sp.inWaiting()))
                                
                            if (len(resetFFWorkTimeCounterCommandResponseData) > 0):
                                resetFFWorkTimeCounterCommandResponse = npbc_communication.resetFFWorkTimeCounterCommand().processResponseData(resetFFWorkTimeCounterCommandResponseData)
                                
                                if (isinstance(resetFFWorkTimeCounterCommandResponse, npbc_communication.failResponse)):
                                    print ("   -> failed")

                                if (isinstance(resetFFWorkTimeCounterCommandResponse, npbc_communication.successResponse)):
                                    print ("   -> success")

                                    params = [response.SwVer, response.Date, response.Mode, response.State, response.Status, response.IgnitionFail, response.PelletJam, response.Tset, response.Tboiler, response.Flame,
                                              response.Heater, response.CHPump,response.DHW, response.BF, response.FF, response.Fan, response.Power, response.ThermostatStop, response.FFWorkTime, response.DhwPump]

                                    dbconn.execute("INSERT INTO [BurnerLogs] ([Timestamp], [SwVer], [Date], [Mode], [State], [Status], [IgnitionFail], [PelletJam], [Tset], [Tboiler], [Flame], \
                                                           [Heater],[CHPump],[DHW],  [BF], [FF], [Fan], [Power], [ThermostatStop], [FFWorkTime], [DhwPump]) VALUES (datetime(), ?, ?, ?, ?, ?, ?, ?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", params)
                                    dbconn.commit()

                        else:
                            params = [response.SwVer, response.Date, response.Mode, response.State, response.Status, response.IgnitionFail, response.PelletJam, response.Tset, response.Tboiler, response.Flame,
                                      response.Heater, response.CHPump, response.DHW, response.BF, response.FF, response.Fan, response.Power, response.ThermostatStop, response.FFWorkTime, response.DhwPump]

                            dbconn.execute("INSERT INTO [BurnerLogs] ([Timestamp], [SwVer], [Date], [Mode], [State], [Status], [IgnitionFail], [PelletJam], [Tset], [Tboiler], [Flame], \
                                                   [Heater], [CHPump], [DHW], [BF], [FF], [Fan], [Power], [ThermostatStop], [FFWorkTime], [DhwPump]) VALUES (datetime(), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", params)
                            dbconn.commit()

            except Exception as e1:
                print ("error communicating...: " + str(e1))

            time.sleep(15)
			