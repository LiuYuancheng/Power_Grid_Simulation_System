#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        scadaDataMgr.py
#
# Purpose:     Data manager module used for connecting to the OT device module 
#              (PLC and RTU) to set and monitor the device state. It will also 
#              control all the other data processing modules and store the result 
#              or interprocess data.
#
# Author:      Yuancheng Liu
#
# Created:     2024/09/03
# Version:     v0.0.2
# Copyright:   Copyright (c) 2024 LiuYuancheng
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

        # Init the PLC client to connect to the PLC.
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
                gv.gDebugPrint('DataManager: Connected to PLC %s' %str(plcIpaddr), 
                               logType=gv.LOG_INFO)
                self.plcConnectionState[key] = True
            else:
                gv.gDebugPrint('DataManager: Fail to connect to PLC %s' %str(plcIpaddr),
                               logType=gv.LOG_INFO)
                self.plcConnectionState[key] = False
            self.regsDict[key] = []
            self.coilsDict[key] = []

        # Init the RTU client to connect to the RTU.
        self.rtuClient = snap7Comm.s7CommClient(gv.RTU_IP, rtuPort=gv.RTU_PORT, 
                                                snapLibPath=gv.gS7snapDllPath)
        self.rtuConnectionState = self.rtuClient.checkConn()
        self.regsStateRW = OrderedDict() # RTU index to read/write
        self.regsStateRW['solar']   = 1
        self.regsStateRW['wind']    = 2
        self.regsStateRW['gen1']    = 3
        self.regsStateRW['gen2']    = 4
        self.regsStateRW['gen3']    = 5
        self.regsStateRW['transM']  = 6
        self.regsStateRW['load1']   = 7
        self.regsStateRW['load2']   = 8
        # RTU data dictionary
        self.rtuDataDict = {
            'solar':    [0, 0, 0, 0],
            'wind':     [0, 0, 0, 0],
            'gen1':     [0, 0, 0, 0],
            'gen2':     [0, 0, 0, 0],
            'gen3':     [0, 0, 0, 0],
            'transM':   [0, 0, 0, 0],
            'load1':    [0, 0, 0, 0],
            'load2':    [0, 0, 0, 0]
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
        
    def checkloadError(self):
        transmRangeV, transmRangeC = (0, 150), (0, 120)
        load1RangeV, load1RangeC = (0, 80), (0, 110)
        load2RangeV, load2RangeC = (0, 15), (0, 90)
        load3RangeV, load3RangeC = (0, 230), (0, 40)
        # Check tramission load error
        transmV, transmC = self.rtuDataDict['transM'][2], self.rtuDataDict['transM'][3]
        if not (transmRangeV[0] <= transmV <= transmRangeV[1]):
            if gv.iDataDisPanel: gv.iDataDisPanel.updateErrorCode('V0')
            gv.iMainFrame.updateTFDetail("Error: Measured transmission voltage %s Kv out of safety range!" %str(transmV))
            gv.iMainFrame.updateTFDetail("Active safety mechanism : Transmission out cut off!.")
            gv.idataMgr.setPlcCoilsData('PLC-00', int(15), False)
            return True
    
        if not (transmRangeC[0] <= transmC <= transmRangeC[1]):
            if gv.iDataDisPanel: gv.iDataDisPanel.updateErrorCode('C0')
            gv.iMainFrame.updateTFDetail("Error: Measured transmission current %s Kv out of safety range!" %str(transmC)) 
            gv.iMainFrame.updateTFDetail("Active safety mechanism: Transmission out cut off!.")
            gv.idataMgr.setPlcCoilsData('PLC-00', int(15), False)
            return True
            
        load1V, load1C = self.rtuDataDict['load1'][2], self.rtuDataDict['load1'][3]
        if not (load1RangeV[0] <= load1V <= load1RangeV[1]):
            if gv.iDataDisPanel: gv.iDataDisPanel.updateErrorCode('V1')
            gv.iMainFrame.updateTFDetail("Error: Measured load1 voltage %s Kv out of safety range!" %str(load1V))
            gv.iMainFrame.updateTFDetail("Active safety mechanism: Load1 out cut off!.")
            gv.idataMgr.setPlcCoilsData('PLC-00', int(19), False)
            return True

        if not (load1RangeC[0] <= load1C <= load1RangeC[1]):
            if gv.iDataDisPanel: gv.iDataDisPanel.updateErrorCode('C1')
            gv.iMainFrame.updateTFDetail("Error: Measured load1 current %s Kv out of safety range!" %str(load1C))
            gv.iMainFrame.updateTFDetail("Active safety mechanism: Load1 out cut off!.")
            gv.idataMgr.setPlcCoilsData('PLC-00', int(19), False)
            return True
        
        load2V, load2C = self.rtuDataDict['load2'][0], self.rtuDataDict['load2'][1]
        if not (load2RangeV[0] <= load2V <= load2RangeV[1]):
            if gv.iDataDisPanel: gv.iDataDisPanel.updateErrorCode('V2')
            gv.iMainFrame.updateTFDetail("Error: Measured load2 voltage %s Kv out of safety range!" %str(load2V))
            gv.iMainFrame.updateTFDetail("Active safety mechanism: Load2 out cut off!.")
            gv.idataMgr.setPlcCoilsData('PLC-00', int(20), False)
            return True

        if not (load2RangeC[0] <= load2C <= load2RangeC[1]):
            if gv.iDataDisPanel: gv.iDataDisPanel.updateErrorCode('C2')
            gv.iMainFrame.updateTFDetail("Error: Measured load2 current %s Kv out of safety range!" %str(load2C))
            gv.iMainFrame.updateTFDetail("Active safety mechanism: Load2 out cut off!.")
            gv.idataMgr.setPlcCoilsData('PLC-00', int(20), False)
            return True
        
        load3V, load3C = self.rtuDataDict['load2'][2], self.rtuDataDict['load2'][3]
        if not (load3RangeV[0] <= load3V <= load3RangeV[1]):
            if gv.iDataDisPanel: gv.iDataDisPanel.updateErrorCode('V3')
            gv.iMainFrame.updateTFDetail("Error: Measured load3 voltage %s Kv out of safety range!" %str(load3V))
            gv.iMainFrame.updateTFDetail("Active safety mechanism: Load3 out cut off!.")
            gv.idataMgr.setPlcCoilsData('PLC-00', int(18), False)
            return True
        
        if not (load3RangeC[0] <= load3C <= load3RangeC[1]):
            if gv.iDataDisPanel: gv.iDataDisPanel.updateErrorCode('C3')
            gv.iMainFrame.updateTFDetail("Error: Measured load3 current %s Kv out of safety range!" %str(load3C))
            gv.iMainFrame.updateTFDetail("Active safety mechanism: Load3 out cut off!.")
            gv.idataMgr.setPlcCoilsData('PLC-00', int(18), False)
            return True
        return False

    #-----------------------------------------------------------------------------
    # define all the get() function here.
    def getPlcConntionState(self, plcID):
        """ Return the PLC connection state."""
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
    def fetchRTUdata(self):
        """ Connect to RTU to fetch the data."""
        for key in self.regsStateRW.keys():
            memoryIdx = self.regsStateRW[key]
            rtuDataList = self.rtuClient.readAddressVal(memoryIdx, dataIdxList = (0, 2, 4, 6), 
                                                        dataTypeList=[INT_TYPE, INT_TYPE, INT_TYPE, INT_TYPE])
            self.rtuDataDict[key] = rtuDataList.copy()
        print(self.rtuDataDict)

    #-----------------------------------------------------------------------------
    def getRtuConnectionState(self):
        return self.rtuConnectionState

    #-----------------------------------------------------------------------------
    def getAllRtuDataDict(self):
        return self.rtuDataDict

    #-----------------------------------------------------------------------------
    def getPowerGenerated(self):
        """ Return the total power generated KW (int) by all the generators based 
            on the RTU reading data.
        """
        solarVal = self.rtuDataDict['solar'][2]*self.rtuDataDict['solar'][3]
        windVal = self.rtuDataDict['wind'][2]*self.rtuDataDict['wind'][3]
        gen1Val = self.rtuDataDict['gen1'][1]*self.rtuDataDict['gen1'][2]
        gen2Val = self.rtuDataDict['gen2'][1]*self.rtuDataDict['gen2'][2]
        gen3Val = self.rtuDataDict['gen3'][1]*self.rtuDataDict['gen3'][2]
        return int(solarVal+windVal+gen1Val+gen2Val+gen3Val)
    
    #-----------------------------------------------------------------------------
    def getPowerConsumed(self):
        """ Return the total power consumed KW (int) by all the loads based on the 
            RTU reading data.
        """
        loadAgents = gv.iMapMgr.getLoads()
        load1Val = self.rtuDataDict['load1'][2]*self.rtuDataDict['load1'][3] if loadAgents[0].getCtrlState() else 0
        load2Val = self.rtuDataDict['load2'][0]*self.rtuDataDict['load2'][1] if loadAgents[1].getCtrlState() else 0
        load3Val = self.rtuDataDict['load2'][2]*self.rtuDataDict['load2'][3]//1000 if loadAgents[2].getCtrlState() else 0
        return int (load1Val+load2Val+load3Val)

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
    def stop(self):
        for client in self.plcClients.values():
            client.close()
        gv.gDebugPrint('DataManager: Stopped all PLC clients', logType=gv.LOG_INFO)
