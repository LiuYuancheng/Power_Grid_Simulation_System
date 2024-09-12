#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        plcSimulatorTrain.py
#
# Purpose:     A simple plc simulation module to connect and control the real-world 
#              emulator via UDP (to simulate the eletrical signals change) and handle
#              SCADA system Modbus TCP request.
#              - This module will simulate 2 PLCs connected under master-slave mode
#              to sense the train speed and control the trains power
#               
# Author:      Yuancheng Liu
#
# Created:     2023/05/29
# Version:     v0.1.2
# Copyright:   Copyright (c) 2023 Singapore National Cybersecurity R&D Lab LiuYuancheng
# License:     MIT License
#-----------------------------------------------------------------------------
""" 
    Program design:
        We want to create a PLC simulator which can simulate a PLC set (Master[slot-0], 
        Slave[slot-1]) with thress 16-in 8-out PLCs. The PLC sets will take 10 input 
        speed sensor and provide 10 power output signal to implement the railway trains 
        control system.
"""

from collections import OrderedDict

import plcSimGlobalPwr as gv
import modbusTcpCom
import plcSimulator

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class onlyCoilLadderLogic(modbusTcpCom.ladderLogic):
    """ Indiviaul holder register and coil usage, no executable ladder logic 
        between them.
    """
    def __init__(self, parent, ladderName) -> None:
        super().__init__(parent, ladderName=ladderName)

    def initLadderInfo(self):
        self.holdingRegsInfo['address'] = 0
        self.holdingRegsInfo['offset'] = 21
        self.srcCoilsInfo['address'] = None
        self.srcCoilsInfo['offset'] = None
        self.destCoilsInfo['address'] = 0
        self.destCoilsInfo['offset'] = 21
        # For total 10 holding registers connected addresses
        # address: 0 - 3: weline trains speed.
        # address: 4 - 6: nsline trains speed.
        # address: 7 - 9: ccline trains speed.

#-----------------------------------------------------------------------------
    def runLadderLogic(self, regsList, coilList=None):
        if gv.gCoilSychCount == 0: return None 
        coilsRsl = []
        if len(regsList) != 21:
            gv.gDebugPrint('runLadderLogic(): input not valid', logType=gv.LOG_WARN)
            gv.gDebugPrint("Input registers list: %s" %str(regsList))
        else:
            # direct connection copy the register state to coil directly:
            coilsRsl = list(regsList).copy()
            gv.gCoilSychCount -=1
        gv.gDebugPrint('Finished calculate all coils: %s' %str(coilsRsl), logType=gv.LOG_INFO)
        return coilsRsl
        
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class powerPlcSet(plcSimulator.plcSimuInterface):
    """ A PlC simulator to provide below functions: 
        - Create a modbus service running in subthread to handle the SCADA system's 
            modbus requirment.
        - Connect to the real world emulator to fetch the sensor state and calculate 
            the output coils state based on the ladder logic. 
        - Send the signal setup request to the real world emulator to change the signal.
    """
    def __init__(self, parent, plcID, addressInfoDict, ladderObj, updateInt=0.6):
        super().__init__(parent, plcID, addressInfoDict, ladderObj,
                        updateInt=updateInt)

    def _initInputState(self):
        self.regsAddrs = (0, 21)
        self.regSRWfetchKey = gv.gRealWorldKey
        self.regs2RWmap = OrderedDict()
        self.regs2RWmap['allswitch'] = (0, 21)
        self.regsStateRW = OrderedDict()
        self.regsStateRW['allswitch'] = [0]*21

    def _initCoilState(self):
        self.coilsAddrs = (0, 21)
        self.coilsRWSetKey = gv.gRealWorldKey
        self.coils2RWMap = OrderedDict()
        self.coils2RWMap['allswitch'] = (0, 21)
        self.coilStateRW = OrderedDict()
        self.coilStateRW['allswitch']  = [False]*21

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
def main():
    gv.gDebugPrint("Start Init the PLC: %s" %str(gv.PLC_NAME), logType=gv.LOG_INFO)
    gv.iLadderLogic = onlyCoilLadderLogic(None, ladderName='only_coil_control')
    addressInfoDict = {
        'hostaddress': gv.gModBusIP,
        'realworld':gv.gRealWorldIP, 
        'allowread':gv.ALLOW_R_L,
        'allowwrite': gv.ALLOW_W_L
    }
    plc = powerPlcSet(None, gv.PLC_NAME, addressInfoDict,  gv.iLadderLogic)
    plc.run()

if __name__ == "__main__":
    main()
