#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        plcSimulatorPwr.py
#
# Purpose:     A simple plc simulation module to connect and control the real-world 
#              emulator via UDP (to simulate the eletrical signals change) and handle
#              SCADA system Modbus TCP request.
#              - This module will simulate 3 PLCs connected under master-slave mode
#              to control the circuit breaker in the power grid system
#               
# Author:      Yuancheng Liu
#
# Created:     2024/07/29
# Version:     v0.0.2
# Copyright:   Copyright (c) 2024 LiuYuancheng
# License:     MIT License
#-----------------------------------------------------------------------------
""" 
    Program design:
        We want to create a PLC simulator which can simulate a PLC set (Master[slot-0], 
        Slave[slot-1], Slave[slot-2]) with 8-in 8-out PLCs. The PLC sets will take 21 
        physical world breaker's state and control the breaker's state.
    The 21 PLC contact connection (<contact_idx>:<physical world Item> - <HMI-Item>):
    0: Solar switch - GenSW-4
    1: Wind switch - GenSW-5
    2: Stepup Transformer switch 1 - TransUp-2
    3: Stepup Transformer switch 2 - TransUp-3
    4: Stepup Transformer switch 3 - TransUp-1
    5: Motor 1 on/off switch - Motor-1
    6: Motor 2 on/off switch - Motor-2
    7: Motor 3 on/off switch - Motor-3
    8: Motor 1 to Gen1 switch - MotorSW-1
    9: Motor 2 to Gen2 switch - MotorSW-2
    10: Motor 3 to Gen3 switch - MotorSW-3
    11: Gen1 output switch - GenSW-1
    12: Gen2 output switch - GenSW-2
    13: Gen3 output switch - GenSW-3
    14: Transmission Input swith - TranMSW-I
    15: Transmission Output swith - TranMSW-O
    16: Distribution Transformer switch 1 - TransDSW-1
    17: Distribution Transformer switch 2 - TransDSW-2
    18: Distribution Transformer switch 3 - LoadSW-3
    19: Load railway switch - LoadSW-1
    20: Load factory switch - LoadSW-2
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

#-----------------------------------------------------------------------------
    def runLadderLogic(self, regsList, coilList=None):
        if gv.gCoilSychCount == 0: return None # sychronize the coil state with the real world at the 1st when PLC connected to physical world
        coilsRsl = []
        if len(regsList) != 21:
            gv.gDebugPrint('runLadderLogic(): input not valid', logType=gv.LOG_WARN)
            gv.gDebugPrint("Input registers list: %s" %str(regsList))
        else:
            # direct connection copy the register state to coil directly:
            coilsRsl = list(regsList).copy()
            gv.gCoilSychCount = 0
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
        self.coilStateRW['allswitch'] = [False]*21

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
def main():
    gv.gDebugPrint("Start Init the PLC: %s" %str(gv.PLC_NAME), logType=gv.LOG_INFO)
    gv.iLadderLogic = onlyCoilLadderLogic(None, ladderName='only_coil_control')
    addressInfoDict = {
        'hostaddress':  gv.gModBusIP,
        'realworld':    gv.gRealWorldIP, 
        'allowread':    gv.ALLOW_R_L,
        'allowwrite':   gv.ALLOW_W_L
    }
    plc = powerPlcSet(None, gv.PLC_NAME, addressInfoDict,  gv.iLadderLogic)
    plc.run()

if __name__ == "__main__":
    main()
