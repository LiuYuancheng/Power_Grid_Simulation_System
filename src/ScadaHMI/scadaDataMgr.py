#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        scadaDataMgr.py
#
# Purpose:     Data manager module used to control all the other data processing 
#              modules and store the interprocess /result data.
#
# Author:      Yuancheng Liu
#
# Created:     2023/06/13
# Version:     v0.1.2
# Copyright:   Copyright (c) 2023 Singapore National Cybersecurity R&D Lab LiuYuancheng
# License:     MIT License
#-----------------------------------------------------------------------------

import time
from collections import OrderedDict

import scadaGobal as gv
import modbusTcpCom
import snap7Comm
from snap7Comm import BOOL_TYPE, INT_TYPE, REAL_TYPE

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class DataManager(object):
    """ The data manager is a module running parallel with the main thread to 
        connect to PLCs to do the data communication with modbus TCP.
    """
    def __init__(self, parent, plcInfo) -> None:
        self.parent = parent
        self.plcClients = OrderedDict()
        self.regsDict = {}
        self.coilsDict = {}
        self.plcInfo = plcInfo
        self.plcConnectionState = {}
        for key, val in plcInfo.items():
            plcIpaddr = val['ipaddress']
            plcPort = val['port']
            self.plcClients[key] = modbusTcpCom.modbusTcpClient(plcIpaddr, tgtPort=plcPort)
            if self.plcClients[key].checkConn():
                gv.gDebugPrint('DataManager: Connected to PLC', logType=gv.LOG_INFO)
                self.plcConnectionState[key] = True
            else:
                gv.gDebugPrint('DataManager: Fail to connect to PLC', logType=gv.LOG_INFO)
                self.plcConnectionState[key] = False
            self.regsDict[key] = []
            self.coilsDict[key] = []

        # Init the RTU client
        self.rtuClient = snap7Comm.s7CommClient(gv.RTU_IP, rtuPort=gv.RTU_PORT, 
                                                snapLibPath=gv.gS7snapDllPath)
        self.rtuConnectionState = self.rtuClient.checkConn()
        self.regsStateRW = OrderedDict()
        self.regsStateRW['solar'] = 1
        self.regsStateRW['wind'] = 2
        self.regsStateRW['gen1'] = 3
        self.regsStateRW['gen2'] = 4
        self.regsStateRW['gen3'] = 5
        self.regsStateRW['transM'] = 6
        self.regsStateRW['load1'] = 7
        self.regsStateRW['load2'] = 8
        
        self.rtuDataDict = {
            'solar': [0, 0, 0, 0],
            'wind': [0, 0, 0, 0],
            'gen1': [0, 0, 0, 0],
            'gen2': [0, 0, 0, 0],
            'gen3': [0, 0, 0, 0],
            'transM': [0, 0, 0, 0],
            'load1': [0, 0, 0, 0],
            'load2': [0, 0, 0, 0]
        }
        gv.gDebugPrint('ScadaHMI dataMgr inited', logType=gv.LOG_INFO)

    #-----------------------------------------------------------------------------
    def periodic(self, now):
        """ Call back every periodic time."""
        gv.gDebugPrint('DataManager: get PLC information', logType=gv.LOG_INFO)
        for key, val in self.plcClients.items():
            hRegsAddr, hRegsNum = self.plcInfo[key]['hRegsInfo']
            self.regsDict[key] = self.plcClients[key].getHoldingRegs(hRegsAddr, hRegsNum)
            coilsAddr, coilsNum = self.plcInfo[key]['coilsInfo']
            self.coilsDict[key] = self.plcClients[key].getCoilsBits(coilsAddr, coilsNum)
            if self.regsDict[key] is None or self.coilsDict[key] is None:
                self.plcConnectionState[key] = False
            else:
                self.plcConnectionState[key] = True
        self.fetchRTUdata()

    def getPowerGenerated(self):
        solarVal = self.rtuDataDict['solar'][2]*self.rtuDataDict['solar'][3]
        windVal = self.rtuDataDict['wind'][2]*self.rtuDataDict['wind'][3]
        gen1Val = self.rtuDataDict['gen1'][1]*self.rtuDataDict['gen1'][2]
        gen2Val = self.rtuDataDict['gen2'][1]*self.rtuDataDict['gen2'][2]
        gen3Val = self.rtuDataDict['gen3'][1]*self.rtuDataDict['gen3'][2]
        return int(solarVal+windVal+gen1Val+gen2Val+gen3Val)
    
    def getPowerConsumed(self):
        loadAgents = gv.iMapMgr.getLoads()
        load1Val = self.rtuDataDict['load1'][2]*self.rtuDataDict['load1'][3] if loadAgents[0].getCtrlState() else 0
        load2Val = self.rtuDataDict['load2'][0]*self.rtuDataDict['load2'][1] if loadAgents[1].getCtrlState() else 0
        load3Val = self.rtuDataDict['load2'][2]*self.rtuDataDict['load2'][3]//1000 if loadAgents[2].getCtrlState() else 0
        return int (load1Val+load2Val+load3Val)

    #-----------------------------------------------------------------------------
    # define all the get() function here.
    def getConntionState(self, plcID):
        if plcID in self.plcClients.keys():
            return self.plcClients[plcID].checkConn() and self.plcConnectionState[plcID]
        return False

    #-----------------------------------------------------------------------------
    def getPlcHRegsData(self, plcid, startIdx, endIdx):
        if plcid in self.regsDict.keys():
            if not self.regsDict[plcid] is None:
                return self.regsDict[plcid][startIdx:endIdx]
        return None

    #-----------------------------------------------------------------------------
    def getPlcCoilsData(self, plcid, startIdx, endIdx):
        if plcid in self.coilsDict.keys():
            if not self.coilsDict[plcid] is None:
                return self.coilsDict[plcid][startIdx:endIdx]
        return None

    #-----------------------------------------------------------------------------
    def setPlcCoilsData(self, plcid, idx, val):
        """ Set the PLC coils state
            Args:
                plcid (str): PLC ID
                idx (int): coils address index.
                val (bool): coil on/off state.
        """
        if plcid in self.plcClients.keys():
            gv.gDebugPrint('DataManager: set PLC coil:%s' %str((plcid, idx, val)), 
                           logType=gv.LOG_INFO)
            self.plcClients[plcid].setCoilsBit(idx, val)
            time.sleep(0.1)

    #-----------------------------------------------------------------------------
    def fetchRTUdata(self):
        for key in self.regsStateRW.keys():
            memoryIdx = self.regsStateRW[key]
            rtuDataList = self.rtuClient.readAddressVal(memoryIdx, dataIdxList = (0, 2, 4, 6), 
                                                        dataTypeList=[INT_TYPE, INT_TYPE, INT_TYPE, INT_TYPE])
            self.rtuDataDict[key] = rtuDataList.copy()
        print(self.rtuDataDict)

    def getAllRtuDataDict(self):
        return self.rtuDataDict

    def getRtuConnectionState(self):
        return self.rtuConnectionState

    def stop(self):
        for client in self.plcClients.values():
            client.close()
        gv.gDebugPrint('DataManager: Stopped all PLC clients', logType=gv.LOG_INFO)