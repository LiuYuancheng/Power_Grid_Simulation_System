#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        rtuSimulatorTrain.py
#
# Purpose:     A simple rtu simulation module to collect the sensor data from 
#              real-world emulation App via UDP (to simulate the eletrical signals 
#              change) and handle SCADA system S7COmm request.
#                       
# Author:      Yuancheng Liu
#
# Created:     2024/04/05
# Version:     v0.1.4
# Copyright:   Copyright (c) 2024 LiuYuancheng
# License:     MIT License
#-----------------------------------------------------------------------------
""" Program design:
        We want to create a RTU simulator which can simulate a on Train RTU to 
        collect 10 trains's 40 sensor data includes train speed, fron train 
        collision sensor state, train voltage, train current and send to the train 
        control HMI via S7comm protocol.
"""

from collections import OrderedDict
import rtuSimGlobalPower as gv

import snap7Comm
import rtuSimulator
from snap7Comm import BOOL_TYPE, INT_TYPE, REAL_TYPE
        
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class trainPowerRtu(rtuSimulator.rtuSimuInterface):
    """ A RTU simulator to provide below functions: 
        - Create a S7comm service running in subthread to handle the SCADA system's 
            data fetch requirment.
        - Connect to the real world emulator to fetch the sensor state.
    """
    def __init__(self, parent, rtuID, addressInfoDict, dllPath=None, updateInt=0.6):
        super().__init__(parent, rtuID, addressInfoDict, dllPath=dllPath, updateInt=updateInt)

    def _initRealWorldConnectionParm(self):
        """ Init the real world data fetch identify key."""
        self.regSRWfetchKey = gv.gRealWorldKey

    def _initMemoryAddrs(self):
        self.regsStateRW = OrderedDict()
        self.regsStateRW['solar'] = 1
        self.regsStateRW['wind'] = 2
        self.regsStateRW['gen1'] = 3
        self.regsStateRW['gen2'] = 4
        self.regsStateRW['gen3'] = 5
        self.regsStateRW['transM'] = 6
        self.regsStateRW['load1'] = 7
        self.regsStateRW['load2'] = 8
        
        s7commServer = self.s7Service.getS7ServerRef()
        s7commServer.initNewMemoryAddr(1, [0, 2, 4, 6], [INT_TYPE, INT_TYPE, INT_TYPE, INT_TYPE])
        s7commServer.initNewMemoryAddr(2, [0, 2, 4, 6], [INT_TYPE, INT_TYPE, INT_TYPE, INT_TYPE])
        s7commServer.initNewMemoryAddr(3, [0, 2, 4, 6], [INT_TYPE, INT_TYPE, INT_TYPE, INT_TYPE])
        s7commServer.initNewMemoryAddr(4, [0, 2, 4, 6], [INT_TYPE, INT_TYPE, INT_TYPE, INT_TYPE])
        s7commServer.initNewMemoryAddr(5, [0, 2, 4, 6], [INT_TYPE, INT_TYPE, INT_TYPE, INT_TYPE])
        s7commServer.initNewMemoryAddr(6, [0, 2, 4, 6], [INT_TYPE, INT_TYPE, INT_TYPE, INT_TYPE])
        s7commServer.initNewMemoryAddr(7, [0, 2, 4, 6], [INT_TYPE, INT_TYPE, INT_TYPE, INT_TYPE])
        s7commServer.initNewMemoryAddr(8, [0, 2, 4, 6], [INT_TYPE, INT_TYPE, INT_TYPE, INT_TYPE])

    def _initLadderHandler(self):
        self.s7Service.setLadderHandler(None)

    def _updateMemory(self, result):
        """ Update the memory address value when get data from the real world sensors."""
        s7commServer = self.s7Service.getS7ServerRef()
        print(result)
        for key, value in self.regsStateRW.items():
            memoryIdx = value
            rstData = result[key]
            s7commServer.setMemoryVal(memoryIdx, 0, rstData[0])
            s7commServer.setMemoryVal(memoryIdx, 2, rstData[1])
            s7commServer.setMemoryVal(memoryIdx, 4, rstData[2])
            s7commServer.setMemoryVal(memoryIdx, 6, rstData[3])

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
def main():
    gv.gDebugPrint("Start Init the RTU: %s" %str(gv.RTU_NAME), logType=gv.LOG_INFO)
    addressInfoDict = {
        'hostaddress': gv.gS7serverIP,
        'realworld': gv.gRealWorldIP,
    }
    rtu = trainPowerRtu(None, gv.RTU_NAME, addressInfoDict,
                        dllPath=gv.gS7snapDllPath, updateInt=gv.gInterval)
    rtu.run()

#-----------------------------------------------------------------------------
if __name__ == "__main__":
    main()
