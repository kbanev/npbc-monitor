#!/usr/bin/python3

import os
import time
import multiprocessing
from multiprocessing.managers import BaseManager
import serialworker
import json
import sqlite3
import settings
import npbc_communication

def initializeDatabase():
    dbconn = sqlite3.connect(settings.DATABASE)
    dbconn.execute("CREATE TABLE IF NOT EXISTS [BurnerLogs] ( \
                           [Timestamp] DATETIME NOT NULL PRIMARY KEY, \
                           [SwVer] NVARCHAR NOT NULL, \
                           [Date] DATETIME NOT NULL, \
                           [Mode] INTEGER NOT NULL, \
                           [State] INTEGER NOT NULL, \
                           [Status] INTEGER NOT NULL, \
                           [IgnitionFail] TINYINT NOT NULL, \
                           [PelletJam] TINYINT NOT NULL, \
                           [Tset] INTEGER NOT NULL, \
                           [Tboiler] INTEGER NOT NULL, \
                           [Flame] INTEGER NOT NULL, \
                           [Heater] TINYINT NOT NULL, \
                           [DhwPump] TINYINT NOT NULL, \
                           [DHW] TINYINT NOT NULL, \
                           [CHPump] TINYINT NOT NULL, \
                           [BF] TINYINT NOT NULL, \
                           [FF] TINYINT NOT NULL, \
                           [Fan] INTEGER NOT NULL, \
                           [Power] INTEGER NOT NULL, \
                           [ThermostatStop] TINYINT NOT NULL, \
                           [FFWorkTime] INTEGER NOT NULL)")
    dbconn.commit()

if __name__ == '__main__':
    ## Initialize database
    initializeDatabase()

    ## start the serial worker in background (as a deamon)
    sp = serialworker.SerialProcess()
    #sp.daemon = True
    sp.start()
